import time
import datetime
import netCDF4
import numpy as np
import os
from thredds_crawler.crawl import Crawl

from django.contrib.gis.geos import GEOSGeometry

from geospaas.utils import validate_uri

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


def crawl(url):
    c = Crawl(url, select=['.*meta.nc'], skip=None, debug=None)
    locsite = []
    
    for jr in c.datasets:
        locsite.append(str(jr.id))
    rdro = ['http://tds0.ifremer.fr/thredds/catalog/' + '/'.join(jj.split('/')[:-1]) + '/catalog.html' for jj in locsite]
#    print (rdro)

    #print ('the new data is',rdro[0:1])
    gd = 0
    sitenamerd=[]
    added=0
    for kk in rdro:
    #for kk in rdro[0:4]: 
        urd = rdro[gd]
        crr = Crawl(urd, select=None, skip=['.*meta.nc', '.*Rtraj.nc', '.*tech.nc'], debug=None)
        gd += 1

        for pp in crr.datasets:
            #print (pp.id)
            sitenamerd.append(['http://tds0.ifremer.fr/thredds/dodsC/'+ str(pp.id)])
            uricorrect='http://tds0.ifremer.fr/thredds/dodsC/'+ str(pp.id)
            ds0, cr0 = try_add_argo_float(uricorrect)

            if cr0:
                print ('Added %s, no. %d,%d'%(url, added, len(crr.datasets)))
                added += 1
                print('Added',added)

#            import ipdb
#            ipdb.set_trace() 
#    return sitenamerd	
    return added

def get_data(datauri):
    """ Return data stored in a remote netCDF dataset available via OpenDAP
    Parameters
    ----------
    uri : string
    The full uri of the dataset        

    """        
    print(datauri)
    nc = netCDF4.Dataset(datauri)
    time    = nc.variables['JULD']
    depth = nc.variables['PRES']

    checkdepth = 0
    findepth = np.zeros(time.shape[0])
    for i in range (0, depth.shape[0]):
        maxdepth = np.amax(depth[i])
        findepth[i] = maxdepth
        if (maxdepth > checkdepth):
            dd=i
            checkdepth = maxdepth
        maxdepth = findepth[dd]
    
    temperature = nc.variables['TEMP'][dd]   
    tempadj=nc.variables['TEMP_ADJUSTED'][dd]
    depthnew = nc.variables['PRES'][dd]    
    depthadj = nc.variables['PRES_ADJUSTED'][dd]    

    latitude = nc.variables['LATITUDE'][dd]
    longitude = nc.variables['LONGITUDE'][dd]

    lonm=nc.variables['LONGITUDE'][dd].mask
    latm=nc.variables['LATITUDE'][dd].mask
    timm=nc.variables['JULD'][dd].mask

    if (lonm == True or latm == True):
        longitude=-999.9
        latitude=-999.9


    out = {}
    out['latitude'] = nc.variables.pop('LATITUDE')[dd]
    out['longitude'] = nc.variables.pop('LONGITUDE')[dd]
    out['temperature'] = nc.variables.pop('TEMP')[dd]
    out['temperatureadj'] = nc.variables.pop('TEMP_ADJUSTED')[dd]
    out['salinity'] = nc.variables.pop('PSAL')[dd]
    out['salinityadj'] = nc.variables.pop('PSAL_ADJUSTED')[dd]
    out['depth'] = nc.variables.pop('PRES')[dd]
    out['depthadj'] = nc.variables.pop('PRES_ADJUSTED')[dd]
    
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
