import time
import datetime
import netCDF4
import numpy as np
import os
from thredds_crawler.crawl import Crawl

from django.db.utils import IntegrityError
from django.contrib.gis.geos import GEOSGeometry

from geospaas.utils.utils import validate_uri

from argo_floats.models import ArgoFloats
from geospaas.vocabularies.models import Platform, Instrument, Location
from geospaas.vocabularies.models import  DataCenter, ISOTopicCategory
from geospaas.catalog.models import GeographicLocation, DatasetURI, Source, Dataset

def try_add_argo_float(uricorrect, tries=3):
    ''' Attempt adding argo float several times recursevly with a timeout 
    Parameters
    ----------
    uricorrect : str
        URI of Argo float
    tries : int
        number of tries left

    '''
    try:
        ds, cr = ArgoFloats.objects.get_or_create(uricorrect)  
    except (OSError, ValueError):
        if tries > 0:
            time.sleep(0.5)
            print('Failed to read %s. Retrying...' % uricorrect)
            ds, cr = try_add_argo_float(uricorrect, tries=tries-1)
        else:
            print('Cannot add ', uricorrect)
        ds, cr = None,False            

    return ds, cr

def crawl(url, **options):
    validate_uri(url)

    skips = Crawl.SKIPS + ['.*ncml', '.*meta.nc', '.*Rtraj.nc', '.*tech.nc']
    c = Crawl(url, skip=skips, debug=True)
    added = 0
    for ds in c.datasets:
        url = [s.get('url') for s in ds.services if
                s.get('service').lower()=='opendap'][0]
        metno_obs_stat, cr = ArgoFloats.objects.get_or_create(url)
        if cr:
            added += 1
            print('Added %s, no. %d/%d'%(url, added, len(c.datasets)))
        # Connect all service uris to the dataset
        for s in ds.services:
            try:
                ds_uri, _ = DatasetURI.objects.get_or_create(name=s.get('name'),
                    service=s.get('service'), uri=s.get('url'), dataset=gds)
            except IntegrityError:
                # There is no standard for the name (and possibly the service). This means that the
                # naming defined by geospaas.catalog.managers.DAP_SERVICE_NAME (and assigned to the
                # DatasetURI in geospaas.nansat_ingestor.managers.DatasetManager.get_or_create) may
                # be different from s.get('name').
                # Solution: ignore the error and continue the loop
                continue
    return added

#def crawl(url):
#    c = Crawl(url, select=['.*meta.nc'], skip=None, debug=None)
#    locsite = []
#    
#    for jr in c.datasets:
#        locsite.append(str(jr.id))
#
#    rdro = ['http://tds0.ifremer.fr/thredds/catalog/' + '/'.join(jj.split('/')[:-1]) +
#            '/catalog.html' for jj in locsite]
##    print (rdro)
#    import ipdb
#    ipdb.set_trace()
#
#    #print ('the new data is',rdro[0:1])
#    gd = 0
#    sitenamerd=[]
#    added=0
#    for kk in rdro:
#    #for kk in rdro[0:4]: 
#        urd = rdro[gd]
#        crr = Crawl(urd, select=None, skip=['.*meta.nc', '.*Rtraj.nc', '.*tech.nc'], debug=None)
#        gd += 1
#
#        for pp in crr.datasets:
#            #print (pp.id)
#            sitenamerd.append(['http://tds0.ifremer.fr/thredds/dodsC/'+ str(pp.id)])
#            uricorrect='http://tds0.ifremer.fr/thredds/dodsC/'+ str(pp.id)
#            ds0, cr0 = try_add_argo_float(uricorrect)
#
#            if cr0:
#                print ('Added %s, no. %d,%d'%(url, added, len(crr.datasets)))
#                added += 1
#                print('Added',added)
#
##            import ipdb
##            ipdb.set_trace() 
##    return sitenamerd	
#    return added

def get_data(dataset):
    """ Return data stored in a remote netCDF dataset available via OpenDAP
    Parameters
    ----------
    dataset : geospaas.models.Dataset
    The dataset to retrieve

    """        
    nc = netCDF4.Dataset(dataset.dataseturi_set.all()[0].uri)

    lonm=nc.variables['LONGITUDE'][0].mask
    latm=nc.variables['LATITUDE'][0].mask
    timm=nc.variables['JULD'][0].mask

    if (lonm == True or latm == True):
        longitude=-999.9
        latitude=-999.9


    out = {}
    out['latitude'] = nc.variables.pop('LATITUDE')[0]
    out['longitude'] = nc.variables.pop('LONGITUDE')[0]
    out['temperature'] = nc.variables.pop('TEMP')[0]
    out['temperatureadj'] = nc.variables.pop('TEMP_ADJUSTED')[0]
    out['salinity'] = nc.variables.pop('PSAL')[0]
    out['salinityadj'] = nc.variables.pop('PSAL_ADJUSTED')[0]
    out['depth'] = nc.variables.pop('PRES')[0]
    out['depthadj'] = nc.variables.pop('PRES_ADJUSTED')[0]
    
    return out


def datafilter(timefilt,idargo,year):

    dss=Dataset.objects.all().values()

#.............
#...Extract uri from exact date
#.............

    rrtim=dss.filter(time_coverage_start=timefilt)       
    rr1=rrtim.values('entry_id')
    webid_tim=rr1[0]["entry_id"]

#.................
#.....Extract uri from platform number
#...............

    rrid=dss.filter(entry_title__contains=idargo)
    rr2=rrid.values('entry_id')
    webid_id=[]; 
    for qqq in range(len(rrid)):
        webadd=rr2[qqq]["entry_id"]
        webid_id.append(webadd)


#..................
#...........Extract uri using year
#..............
    
    rrtimyr=dss.filter(time_coverage_start__contains=year)
    rryr=rrtimyr.values('entry_id')
    webid_year=[];
    for qqq1 in range(len(rrtimyr)):
        webaddyr=rryr[qqq1]["entry_id"]
        webid_year.append(webaddyr)    

    return webid_id,webid_tim,webid_year

#    import ipdb
#    ipdb.set_trace()
