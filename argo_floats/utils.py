import datetime
import netCDF4
import numpy as np

from thredds_crawler.crawl import Crawl

from django.contrib.gis.geos import GEOSGeometry

from geospaas.utils import validate_uri

from argo_floats.models import ArgoFloats


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
    #for kk in rdro:
    for kk in rdro[0:4]: 
    # Only first Argo float is called inorder to reduce the computational time. Change it into rdro:
        urd = rdro[gd]
        crr = Crawl(urd, select=None, skip=['.*meta.nc', '.*Rtraj.nc', '.*tech.nc'], debug=None)
        gd += 1

        for pp in crr.datasets:
            #print (pp.id)
            sitenamerd.append(['http://tds0.ifremer.fr/thredds/dodsC/'+ str(pp.id)])
            uricorrect='http://tds0.ifremer.fr/thredds/dodsC/'+ str(pp.id)
            ds0, cr0 = ArgoFloats.objects.get_or_create(uricorrect)

            if cr0:
                print ('Added %s, no. %d,%d'%(url, added, len(crr.datasets)))
                added += 1
                print('Added',added)

#            import ipdb
#            ipdb.set_trace() 
#    return sitenamerd	
    return added
