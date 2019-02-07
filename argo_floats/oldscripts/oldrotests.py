# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import netCDF4

import datetime
from django.test import TestCase

from django.utils.six import StringIO
from django.core.management import call_command
print "works until here"
from  argo_floats.models import ArgoFloats

print "2. works until here"
from argo_floats.utils import crawl

from thredds_crawler.crawl import Crawl

class TestDataset(TestCase):

    fixtures = ['vocabularies', 'catalog']

    def test_getorcreate_opendap_uri(self):

#       .......Netcdf files from nmdis servere has a problem
#       uri ='http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/nmdis/2901633/profiles/R2901633_071.nc'
#       ...........

#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/aoml/7900685/profiles/R7900685_002.nc'
# 	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/meds/4902465/profiles/R4902465_001.nc'
	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kordi/7900181/profiles/R7900181_118.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/kma/7900249/profiles/D7900249_071.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/jma/7900692/profiles/R7900692_052.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/incois/7654321/profiles/R7654321_001.nc'
#        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/csiro/7900629/profiles/R7900629_003.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/csio/5901608/profiles/R5901608_230.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/coriolis/7900594/profiles/R7900594_142.nc'
#	uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/bodc/7900154/profiles/D7900154_122.nc'

        print uri
        ''' Shall open file, read metadata and save'''
        nc = netCDF4.Dataset(uri)

	time    = nc.variables['JULD']
	NewDate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[0])
	print 'The date is: ', NewDate

	ds0, cr0 = ArgoFloats.objects.get_or_create(uri)
        ds1, cr1 = ArgoFloats.objects.get_or_create(uri)

        self.assertTrue(cr0)
        self.assertFalse(cr1)


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
