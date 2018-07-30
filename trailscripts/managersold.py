import numpy as np
import warnings
import datetime
import os
import pythesint as pti
import netCDF4
from django.db import models
from django.conf import settings
from django.contrib.gis.geos import LineString

from django.contrib.gis.geos import GEOSGeometry
from geospaas.utils import validate_uri, nansat_filename


from geospaas.vocabularies.models import Platform, Instrument
from geospaas.vocabularies.models import  DataCenter, ISOTopicCategory
from geospaas.catalog.models import GeographicLocation, DatasetURI, Source, Dataset



class ArgoFloatsManager(models.Manager):

	#def set_metadata(self):
        #	pp = Platform.objects.get(short_name='BUOYS')
        #        ii = Instrument.objects.get(short_name='DRIFTING BUOYS')
        #        source = Source.objects.get_or_create(platform=pp, instrument=ii)[0]
        #        dc = DataCenter.objects.get(short_name='DOC/NOAA/OAR/AOML')
        #        iso_category = ISOTopicCategory.objects.get(name='Oceans')
        #        return source, dc, iso_category


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

	# set source
         platform = pti.get_gcmd_platform('BUOYS')
         instrument = pti.get_gcmd_instrument('DRIFTING BUOYS')
         pp = Platform.objects.get(
                category=platform['Category'],
                series_entity=platform['Series_Entity'],
               short_name=platform['Short_Name'],
                long_name=platform['Long_Name']
            )
         ii = Instrument.objects.get(
                category = instrument['Category'],
                instrument_class = instrument['Class'],
                type = instrument['Type'],
                subtype = instrument['Subtype'],
                short_name = instrument['Short_Name'],
                long_name = instrument['Long_Name']
            )
         source = Source.objects.get_or_create(
            platform = pp,
           instrument = ii)[0]

#	dc = DataCenter.objects.get(short_name='NM/ME/KO/KM/JA/IN/CS/HZ/IF/BO/AO')


         dc = DataCenter.objects.get(short_name='DOC/NOAA/OAR/AOML')
	 iso_category = ISOTopicCategory.objects.get(name='Oceans')
	 nc = netCDF4.Dataset(uri)

	 # Time variable read
	 time    = nc.variables['JULD']

	 #Reading depth variable
	 depth = nc.variables['PRES']
	 print 'checking data', depth[0]
	

	 entrytitle = nc.comment

	 print entrytitle
	 # checking whether there is more than one profile data on the same day, Found that data from AOML has this problem 
	 # if there is, then delete the wrong data, In here the shallowest profile is removed
	 # if we check manually we can see that the wrong profile doesnot go beyond 500 meter.

	 checkdepth = 0
	 findepth = np.zeros(time.shape[0])

	 for i in range (0, depth.shape[0]):
         	print i
        	maxdepth = np.amax(depth[i])
		findepth[i] = maxdepth
       		if (maxdepth > checkdepth):
               		dd=i
               		checkdepth = maxdepth
	 maxdepth = findepth[dd]	

	# Reading info about the data center
	 dca = nc.variables['DATA_CENTRE'][dd]
	 dcstr2= ''.join(map(str, dca))
	 datacenter = dcstr2.replace("--", "")
	 print datacenter
	 if (datacenter == 'AO'):
		dcnew = 'AOML'	
	 print dcnew

	 # Reading Platform number
	 platnum = nc.variables['PLATFORM_NUMBER']
	 str2= ''.join(map(str, platnum))
	 platnumnew = str2.replace("--", "")

	 # final Date 
	 newdate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[dd])
	 yearargo = newdate.strftime('%Y')
	 monargo = newdate.strftime('%m')
	 dayargo = newdate.strftime('%d')
	
	 # Reading Lat Lon Variables
	 latitude = nc.variables['LATITUDE'][dd]
	 longitude = nc.variables['LONGITUDE'][dd]
	 location = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
         geolocation = GeographicLocation.objects.get_or_create(geometry=location)[0]
	
	 datamodef = nc.variables['DATA_MODE'][dd]
	 if (datamodef == 'R'):
        	datamode = 'Real time mode'
        	print datamode
	 if (datamodef == 'A'):
        	datamode = 'Delayed time mode'
        	print datamode



         ds = Dataset(
                ISO_topic_category = iso_category,
 	        source = source,
		data_center = dc,
                geographic_location = geolocation,
		)
         ds.save()
         ds_uri = DatasetURI.objects.get_or_create(uri=uri, dataset=ds)[0]
         return ds, True

