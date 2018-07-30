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


class TestDataset(TestCase):

    fixtures = ['vocabularies', 'catalog']

    def test_getorcreate_opendap_uri(self):
        uri = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/aoml/7900685/profiles/R7900685_002.nc'
        ''' Shall open file, read metadata and save'''
        nc = netCDF4.Dataset(uri)

	time    = nc.variables['JULD']
	NewDate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[0])
	print 'The date is: ', NewDate

	ds0, cr0 = ArgoFloats.objects.get_or_create(uri)
        ds1, cr1 = ArgoFloats.objects.get_or_create(uri)

        self.assertTrue(cr0)
        self.assertFalse(cr1)

