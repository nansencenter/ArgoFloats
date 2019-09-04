
import datetime as dt

import numpy as np
from netCDF4 import Dataset
from matplotlib import path
from shapely.geometry import Polygon
from math import sin, cos, sqrt, atan2, radians
#from scipy.interpolate import RegularGridInterpolator
#import matplotlib.pyplot as plt

#from zoning import fill_gaps_nn

# Reading data from the Argo floats
ifilename = '20160128_prof.nc'


ds1 = Dataset(ifilename)
timeargor = ds1['JULD'][:].data
timeargo=np.round(timeargor)

print timeargo.size
#print timeargo

latargo = ds1['LATITUDE'][:].data
lonargo = ds1['LONGITUDE'][:].data
tempargo = ds1['TEMP_ADJUSTED'][:,:].data
salargo = ds1['PSAL_ADJUSTED'][:,:].data
depthargo = ds1['PRES_ADJUSTED'][:,:].data



date10 = dt.datetime(1950,1,1)


#print date10
#print timeargo.size

for ofilename in ['LB-anti-cycloniceddies2016.nc']:
    
	ds2 = Dataset(ofilename)
	y2 = ds2['year'][:].data.astype(int)
	m2 = ds2['month'][:].data.astype(int)
	d2 = ds2['day'][:].data.astype(int)

    

	timeeddy = np.array([(dt.datetime(yy,mm,dd) - date10).days for yy,mm,dd in zip(y2,m2,d2)], dtype=float)
	loneddy = ds2['lon'][:].data
	lateddy = ds2['lat'][:].data
	radeddy = ds2['Radius'][:].data


#import ipdb
#ipdb.set_trace()
	
	print timeargo.shape[0]

	for ii in range(0, timeargo.shape[0]):
	    timeindx = np.where(timeargo[ii] == timeeddy)[0]
	    loneddyN=loneddy[timeindx]
        lateddyN=lateddy[timeindx]
        radeddyN=radeddy[timeindx]

        #print ii
        #print timeargo[ii]
        #print timeindx
        print timeindx.shape[0]
        #print lateddyN

        lat_argo_res = np.zeros((len(latargo), len(lateddyN))).T + latargo
        lon_argo_res = np.zeros((len(lonargo), len(loneddyN))).T + lonargo
        lat_eddy_res = np.zeros((len(latargo), len(lateddyN))) + lateddyN
        lon_eddy_res = np.zeros((len(lonargo), len(loneddyN))) + loneddyN

        lat_eddy_res=lat_eddy_res.T
        lon_eddy_res=lon_eddy_res.T

        latargo_rad=np.radians(lat_argo_res)
        lonargo_rad=np.radians(lon_argo_res)
        lateddy_rad=np.radians(lat_eddy_res)
        loneddy_rad=np.radians(lon_eddy_res)

        # approximate radius of earth in km
        R = 6373.0
        #dlon = lon2 - lon1
        #dlat = lat2 - lat1
        #a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        #c = 2 * atan2(sqrt(a), sqrt(1 - a))
        #distance = R * c
        


        dlon = lonargo_rad - loneddy_rad
        dlat = latargo_rad - lateddy_rad

        a = np.sin(dlat / 2)**2 + np.cos(lateddy_rad) * np.cos(latargo_rad) * np.sin(dlon / 2)**2
        c2 = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c2

        # distance in km, note eddy radius in meter.

        radeddyN=radeddyN/1000

        # Finding whether the Argo float is whithin an eddy. For that the distance between the eddy center and argo float center ....
        # ...should be less than one.
        import ipdb; ipdb.set_trace()

        # dist_min_rad=distance.T - radeddyN
        radeddyN_res = np.zeros((len(latargo), len(lateddyN))) + radeddyN
        dist_min_rad=distance - radeddyN_res.T
        coloc_indx = np.where(dist_min_rad < 1)[0]

        





