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

	 # set source	
        pp = Platform.objects.get(short_name='BUOYS')
        ii = Instrument.objects.get(short_name='DRIFTING BUOYS')
        source = Source.objects.get_or_create(platform=pp, instrument=ii)[0]
         # Note that datacenter is defined inside the loop (see the code below)
        iso_category = ISOTopicCategory.objects.get(name='Oceans')
	 # reading the data
        nc = netCDF4.Dataset(uri)
	 # Time variable read
        time    = nc.variables['JULD']
        import ipdb
        ipdb.set_trace()
        #Reading depth variable
        depth = nc.variables['PRES']
        #print ('checking data', depth[0])
	

	 # checking whether there is more than one profile data on the same day, Found that data from AOML has this problem 
	 # if there is, then delete the wrong data, In here the shallowest profile is removed
	 # if we check manually we can see that the wrong profile doesnot go beyond 500 meter.

        checkdepth = 0
        findepth = np.zeros(time.shape[0])

        for i in range (0, depth.shape[0]):
            maxdepth = np.amax(depth[i])
            findepth[i] = maxdepth
            if (maxdepth > checkdepth):
                dd=i
                checkdepth = maxdepth
        maxdepth = findepth[dd]	

	# Reading info about the data center
        dca = nc.variables['DATA_CENTRE'][dd]
        dcstr2= ''.join(map(str, dca))
        datacenter1 = dcstr2.replace("b", "")
        datacenter = datacenter1.replace("'", "")
        #print (dca)
        print ('datacenter',datacenter)

        #import ipdb
        #ipdb.set_trace()

	#       dc = DataCenter.objects.get(short_name='NM/ME/KO/KM/JA/IN/CS/HZ/IF/BO/AO')
        if (datacenter == 'AO'):
            dc = DataCenter.objects.get(short_name='DOC/NOAA/OAR/AOML')		
        if (datacenter == 'JA'):
            dc = DataCenter.objects.get(short_name='JP/JMA/MRI')
        if (datacenter == 'CS'):
            dc = DataCenter.objects.get(short_name='AU/CSIRO/CLW')
        if (datacenter == 'IF'):
            dc = DataCenter.objects.get(short_name='FR/IFREMER/CORIOLIS')
        if (datacenter == 'BO'):
            dc = DataCenter.objects.get(short_name='UK/NERC/BODC')
        if (datacenter == 'NM'):
            dc = DataCenter.objects.get(bucket_level0=r'ACADEMIC', short_name='', data_center_url='', bucket_level1='')
        if (datacenter == 'ME'):
            dc = DataCenter.objects.get(bucket_level0=r'ACADEMIC', short_name='', data_center_url='', bucket_level1='')
        if (datacenter == 'KO'):
            dc = DataCenter.objects.get(bucket_level0=r'ACADEMIC', short_name='', data_center_url='', bucket_level1='')
        if (datacenter == 'KM'):
            dc = DataCenter.objects.get(bucket_level0=r'ACADEMIC', short_name='', data_center_url='', bucket_level1='')	 
        if (datacenter == 'IN'):
            dc = DataCenter.objects.get(bucket_level0=r'ACADEMIC', short_name='', data_center_url='', bucket_level1='')
        if (datacenter == 'HZ'):
            dc = DataCenter.objects.get(bucket_level0=r'ACADEMIC', short_name='', data_center_url='', bucket_level1='')

        #print (dc)

	 # Reading Platform number
        platnum = nc.variables['PLATFORM_NUMBER'][dd]
#        import ipdb
#        ipdb.set_trace()
        ptstr2= ''.join(map(str, platnum))
        platnum1 = ptstr2.replace("b", "")
        platnum2 = platnum1.replace("'", "")
        platnumnew = platnum2.replace("--", "")
        print ('platform number', platnumnew)
#        import ipdb
#        ipdb.set_trace()
		 
	# final Date 
        #newdate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(float(time[0].data))
        newdate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(int(time[0].data))
        yearargo = newdate.strftime('%Y')
        monargo = newdate.strftime('%m')
        dayargo = newdate.strftime('%d')
	 
	 # Reading Lat Lon Variables
        latitude = nc.variables['LATITUDE'][dd]
        print ('latitude',latitude)
        longitude = nc.variables['LONGITUDE'][dd]
        print ('longitude',longitude)
        location = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
        print ('location',location)
        geolocation = GeographicLocation.objects.get_or_create(geometry=location)[0]

#        import ipdb
#        ipdb.set_trace()
		
        print ('geolocation', geolocation)
        print ('datacenter',dc)
        print ('source',source)

        ds, created = Dataset.objects.get_or_create(
            #entry_id = platnumnew,
            ISO_topic_category = iso_category,
            source = source,
            data_center = dc,
            geographic_location = geolocation,
            time_coverage_start = newdate
            )

        # Also add DatasetParameter (see new code from Jeong-Won)

        ds_uri, ds_uri_created = DatasetURI.objects.get_or_create(uri=uri, dataset=ds)
        return ds, created
