import numpy as np
import warnings
import datetime
import os
import pythesint as pti
import netCDF4
import sys
from django.db import models
from django.conf import settings
from django.contrib.gis.geos import LineString

from django.contrib.gis.geos import GEOSGeometry
from geospaas.utils.utils import validate_uri, nansat_filename


from geospaas.vocabularies.models import Platform, Instrument, Location
from geospaas.vocabularies.models import  DataCenter, ISOTopicCategory
from geospaas.catalog.models import GeographicLocation, DatasetURI, Source, Dataset



class ArgoFloatsManager(models.Manager):


    def get_or_create(self, uri, *args, **kwargs):
        ''' Create dataset and corresponding metadata
         Parameters:
         ----------
         uri : str
         URI to file or stream openable by netCDF4.Dataset
       	 Returns:
         -------
         dataset and flag
         '''
         # check if dataset already exists
        uris = DatasetURI.objects.filter(uri=uri)
        if len(uris) > 0:
            return uris[0].dataset, False
        skips = ['.*ncml', '.*meta.nc', '.*Rtraj.nc', '.*tech.nc']
        import ipdb
        ipdb.set_trace()
        
        nc = netCDF4.Dataset(uri)
        #if nc.dimensions['N_HISTORY'].size == 0:
        #    raise ValueError('Wrong N_HISTORY in ', uri)
	# set source	
        pp = Platform.objects.get(short_name='BUOYS')
        ii = Instrument.objects.get(short_name='DRIFTING BUOYS')
        source = Source.objects.get_or_create(platform=pp, instrument=ii)[0]
        iso_category = ISOTopicCategory.objects.get(name='Oceans')
        # Note that datacenter is defined inside the loop (see the code below)
        time    = nc.variables['JULD']
        depth = nc.variables['PRES']
        #Reading depth variable
	# Reading info about the data center
        dca = nc.variables['DATA_CENTRE'][0]
        dcstr2= ''.join(map(str, dca))
        datacenter1 = dcstr2.replace("b", "")
        datacenter = datacenter1.replace("'", "")

        datacenters = {
            'AO': 'DOC/NOAA/OAR/AOML', 
            'JA': 'JP/JMA/MRI',
            'CS': 'AU/CSIRO/CLW',
            'IF': 'FR/IFREMER/CORIOLIS',
            'BO': 'UK/NERC/BODC',
            'NM': '',
            'ME': '',
            'KO': '',
            'KM': '',
            'IN': '',
            'HZ': '',}
        short_name = datacenters[datacenter]
        
        if (datacenter == 'NM' or 'ME' or 'KO' or 'KM' or 'IN' or 'HZ'):
            dc = DataCenter.objects.get(bucket_level0=r'ACADEMIC', short_name='', data_center_url='', bucket_level1='')
        else:
            dc = DataCenter.objects.get(short_name=short_name)

	 # Reading Platform number
        platnum = nc.variables['PLATFORM_NUMBER'][0]
        ptstr2= ''.join(map(str, platnum))
        platnum1 = ptstr2.replace("b", "")
        platnum2 = platnum1.replace("'", "")
        platnumstr = platnum2.replace("--", "")
        platnumnew =int(platnumstr)

        newdate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(float(time[0].data))
        #newdate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(int(time[0].data))
        yearargo = newdate.strftime('%Y')
        monargo = newdate.strftime('%m')
        dayargo = newdate.strftime('%d')
        
        latitude = nc.variables['LATITUDE'][0]
        longitude = nc.variables['LONGITUDE'][0]
        
        lonm=nc.variables['LONGITUDE'][0].mask
        latm=nc.variables['LATITUDE'][0].mask
        timm=nc.variables['JULD'][0].mask
         
        if (lonm == True or latm == True):
            longitude=-999.9
            latitude=-999.9

       
        location = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
        geolocation = GeographicLocation.objects.get_or_create(geometry=location)[0]
        ds, created = Dataset.objects.get_or_create(
            entry_id = uri,
            entry_title = '%s platform number. %d' % (
                           pp,platnumnew),
#            entry_title = 'platform number. %d' % (platnumnew),
#            entry_title =platnumnew,
            ISO_topic_category = iso_category,
            source = source,
            data_center = dc,
            geographic_location = geolocation,
            time_coverage_start = newdate
            )
         
        ds_uri, ds_uri_created = DatasetURI.objects.get_or_create(uri=uri, dataset=ds)
        return ds, created
