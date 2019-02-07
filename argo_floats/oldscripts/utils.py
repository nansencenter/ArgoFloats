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
    print (rdro)

    #print ('the new data is',rdro[0:1])
    gd = 0
    sitenamerd=[]

    #for kk in rdro:
    for kk in rdro[0:4]: 
    # Only first Argo float is called inorder to reduce the computational time. Change it into rdro:
        urd = rdro[gd]
        crr = Crawl(urd, select=None, skip=['.*meta.nc', '.*Rtraj.nc', '.*tech.nc'], debug=None)
        gd += 1

        for pp in crr.datasets:
            #print (pp.id)
            sitenamerd.append(['http://tds0.ifremer.fr/thredds/dodsC/'+ str(pp.id)])
 
    return sitenamerd	




    #print (c.datasets)
    #for jr in c.datasets:






#def crawl(url, **options):
#    if not validate_uri(url):
#        raise ValueError('Invalid url: %s'%url)

#    if options['year']:
#        select = ['(.*%s\.nc)' %options['year']]
#    elif options['filename']:
#        select = ['(.*%s)' %options['filename']]
#    else:
#
#        select = None

#def crawl(url):
    
#    c = Crawl(url, select=['.*meta.nc'], skip=None, debug=None)
#    i=0
#    locsite = []
#    for jr in c.datasets:
#        print jr.id
#        print 'http://tds0.ifremer.fr/thredds/dodsC/'+str(jr.id)
#        locsite.append(str(jr.id))
#        print i
#        i += 1
#    print locsite
#    rdro = ['/'.join(jj.split('/')[:-1]) for jj in locsite]
#    print rdro

    








#    c = Crawl(url, select=None, skip=['.*meta.nc', '.*Rtraj.nc', '.*Dtraj.nc', '.*tech.nc'], debug=None)
#    added = 0

#    for ds in c.datasets:
#        url = 'http://tds0.ifremer.fr/thredds/dodsC/'+str(ds.id)
#	print url
#        cr = ArgoFloats.objects.get_or_create(url)
#        if cr:
#            print 'Added %s, no. %d/%d'%(url, added, len(c.datasets))
#            added += 1
#    return added

#    for ds in c.datasets:
#        url = [s.get('url') for s in ds.services if
#                s.get('service').lower()=='opendap'][0]
#        ndbc_stdmet, cr = ArgoFloats.objects.get_or_create(url)
#        if cr:
#            print 'Added %s, no. %d/%d'%(url, added, len(c.datasets))
#            added += 1
#    return added

#    url = 'http://tds0.ifremer.fr/thredds/catalog/CORIOLIS-ARGO-GDAC-OBS/nmdis/catalog.html'
#    c = Crawl(url, select=None, skip=['.*meta.nc', '.*Rtraj.nc', '.*tech.nc'], debug=None)
#
#    print c.datasets
#    for jr in c.datasets:
#        print jr.id
#    self.assertEqual(c, 1)
