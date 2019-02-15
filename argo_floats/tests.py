# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from mock import patch

import netCDF4
import datetime
from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command

from geospaas.catalog.models import  Dataset
from argo_floats.models import ArgoFloats
from argo_floats.utils import crawl
from argo_floats.utils import try_add_argo_float
from argo_floats.utils import get_data
from argo_floats.utils import datafilter

#from thredds_crawler.crawl import Crawl

url = 'http://tds0.ifremer.fr/thredds/catalog/CORIOLIS-ARGO-GDAC-OBS/kordi/catalog.html'

class TestDataset(TestCase):
    fixtures = ['vocabularies', 'catalog']

#    def test_getorcreate_opendap_uri(self):
#        added = crawl(url)
#        self.stdout.write(
#        'Successfully added metadata of %s Argo float profiles' %added)
        
    def test_wronglongitude(self):
        fn = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_005.nc'
        ds, cr = ArgoFloats.objects.get_or_create(fn)
   
    @patch('argo_floats.utils.ArgoFloats')    
    def test_failing_ds(self, mockaf):
        mockaf.objects.get_or_create.side_effect = OSError
        fn='http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900121/profiles/R7900121_148.nc'
        ds0, cr0 = try_add_argo_float(fn)
        self.assertIsNone(ds0)
        self.assertFalse(cr0)

    @patch('argo_floats.utils.ArgoFloats')    
    def test_workingfunction(self, mockaf):
        mockaf.objects.get_or_create.return_value = (Dataset(), True)
        fn='http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_006.nc'
        ds, cr = try_add_argo_float(fn)
        self.assertIsInstance(ds, Dataset)
        self.assertTrue(cr)


    def test_read(self):
        f2='http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_006.nc'
        readdata = get_data(f2)
        print('Successfully read data',readdata)
     
    def test_datafilter(self):
        idargo='7900179'
        year='2008'
        timefilt='2008-06-15 16:23:32.000012'

        fn=["http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_006.nc","http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_007.nc","http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_008.nc","http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_009.nc"]
 
        ds=[]
        for ii in range(len(fn)):
            fn[ii]
            ds0, cr0 = try_add_argo_float(fn[ii])
            ds.append(ds0)    

        extractwebid = datafilter(timefilt,idargo,year)

        print(extractwebid)
       
#        print(extdata)


#...............................old................

        # weburi now has links to all the Argo float profiles listed in this server
        # Note that for the time being, only profiles from the first 5 Argo floats are included for computation easiness ...
        # Edit crawl in argo_floats.utils to change the number of Argo floats read  

#        jr=0
#        for rr in weburi:
#            urinew = (''.join(weburi[jr]))
#            print (urinew)
 
#            ds0, cr0 = ArgoFloats.objects.get_or_create(urinew)
#            ds1, cr1 = ArgoFloats.objects.get_or_create(urinew)
 
#            self.assertTrue(cr0)
#            self.assertFalse(cr1)
 
#            jr += 1

#    def test_failing_ds(self):
#        fn = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900179/profiles/R7900179_005.nc'
#        ds, cr = ArgoFloats.objects.get_or_create(fn)




#    def test_crawl(self):
#        print ('url is', url)
#        weburi = crawl(url) 
        
        # weburi now has links to all the Argo float profiles listed in this server
        # Note that for the time only profiles from the first 5 Argo floats are included for computation easiness ...
	# Edit crawl in argo_floats.utils to change the number of Argo floats read  
        	
#        import ipdb
#        ipdb.set_trace()	

#    def test_getorcreate_opendap_uri(self):
#        weburi = crawl(url)
#        jr=0
#        for rr in weburi:
#            urinew = (''.join(weburi[jr]))	    
#            print (urinew)
#            ds0, cr0 = ArgoFloats.objects.get_or_create(urinew)
#            ds1, cr1 = ArgoFloats.objects.get_or_create(urinew)
#            self.assertTrue(cr0)
#            self.assertFalse(cr1)
#            jr += 1

































	    
#    def test_getorcreate_opendap_uri(self):

#        import ipdb
#        ipdb.set_trace()

#        ds0, cr0 = ArgoFloats.objects.get_or_create(uri)
#        ds1, cr1 = ArgoFloats.objects.get_or_create(uri)

#        self.assertTrue(cr0)
#        self.assertFalse(cr1)


#       .......Netcdf files from nmdis servere has a problem
#       uri ='http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/nmdis/2901633/profiles/R2901633_071.nc'
#       ...........

#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/aoml/7900685/profiles/R7900685_002.nc'
#       uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/meds/4902465/profiles/R4902465_001.nc'
#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900181/profiles/R7900181_118.nc'
#        uri = urinew[0]
#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900181/profiles/R7900181_054.nc'
#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900181/profiles/R7900181_054.nc'
#       uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kma/7900249/profiles/D7900249_071.nc'
#       uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/jma/7900692/profiles/R7900692_052.nc'
#       uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/incois/7654321/profiles/R7654321_001.nc'
#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/csiro/7900629/profiles/R7900629_003.nc'
#       uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/csio/5901608/profiles/R5901608_230.nc'
#       uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/coriolis/7900594/profiles/R7900594_142.nc'
#       uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/bodc/7900154/profiles/D7900154_122.nc'

        #print (uri)
#        ''' Shall open file, read metadata and save'''
#        nc = netCDF4.Dataset(uri)

#        time    = nc.variables['JULD']
#        NewDate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(float(time[0].data))
#        print ('The date is: ', NewDate)

#        ds0, cr0 = ArgoFloats.objects.get_or_create(uri)
#        ds1, cr1 = ArgoFloats.objects.get_or_create(uri)

#        self.assertTrue(cr0)
#        self.assertFalse(cr1)







#print ("3. works until here")




    
#    def test_getorcreate_opendap_uri(self):
       #        ''' Shall open file, read metadata and save'''
#        usri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900181/profiles/R7900181_007.nc'
#        ncs = netCDF4.Dataset(''.join(usri))
#        time    = ncs.variables['JULD']
#        NewDate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[0])
#        print 'The date is: ', NewDate

#        ds0, cr0 = ArgoFloats.objects.get_or_create(usri)
#        ds1, cr1 = ArgoFloats.objects.get_or_create(usri)

#        self.assertTrue(cr0)
#        self.assertFalse(cr1)




#print crawl(url)

##website_argo=crawl(url)
##print website_argo

#class TestDataset(TestCase):

#    fixtures = ['vocabularies', 'catalog']
#    uri = website_argo[0] 
#    def test_getorcreate_opendap_uri(self):

#       .......Netcdf files from nmdis servere has a problem
#       uri ='http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/nmdis/2901633/profiles/R2901633_071.nc'
#       ...........

#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/aoml/7900685/profiles/R7900685_002.nc'
# 	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/meds/4902465/profiles/R4902465_001.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900181/profiles/R7900181_118.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kma/7900249/profiles/D7900249_071.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/jma/7900692/profiles/R7900692_052.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/incois/7654321/profiles/R7654321_001.nc'
#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/csiro/7900629/profiles/R7900629_003.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/csio/5901608/profiles/R5901608_230.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/coriolis/7900594/profiles/R7900594_142.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/bodc/7900154/profiles/D7900154_122.nc'


#        ''' Shall open file, read metadata and save'''
#        nc = netCDF4.Dataset(uri)
#        print uri
#	time    = nc.variables['JULD']
#	NewDate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[0])
#	print 'The date is: ', NewDate

#	ds0, cr0 = ArgoFloats.objects.get_or_create(uri)
#        ds1, cr1 = ArgoFloats.objects.get_or_create(uri)

#        self.assertTrue(cr0)
#        self.assertFalse(cr1)


#    def test_crawl(self):
        # For test use kma server for faster run since it has slightly less number of obs, dont use AOML which has the highest
#	url = 'http://tds0.ifremer.fr/thredds/catalog/CORIOLIS-ARGO-GDAC-OBS/kordi/catalog.html'
#	added = crawl(url)
#        self.assertEqual(added, 1)

    #def test_command_crawl(self):
    #    out = StringIO()
    #    url = 'http://dods.ndbc.noaa.gov/thredds/catalog/data/stdmet/catalog.xml'
    #    select = '18ci3h2014.nc' # thredds ID
    #    call_command('crawl_ndbc_stdmet', url, select, stdout=out)
    #    self.assertIn('Successfully added:', out.getvalue())
