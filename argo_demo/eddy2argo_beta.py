from netCDF4 import Dataset
import numpy as np
import datetime as dt 

# for the time being, the script is only made for a single Argo float file. You can use a for loop if you want all data.
ifilename = '20160128_prof.nc'


ds1 = Dataset(ifilename)
timeargor = ds1['JULD'][:]
timeargo = np.round(timeargor)

#print(timeargo.size)
#print timeargo

latargo = ds1['LATITUDE'][:]
lonargo = ds1['LONGITUDE'][:]
tempargo = ds1['TEMP'][:,:]
salargo = ds1['PSAL'][:,:]
depthargo = ds1['PRES'][:,:]

# ok just found that the TEMP_ADJUSTED for the collocated argo float (in the end) on this day is masked...
#Hence I have used TEMP instead of TEMP_ADJUSTED for the demo purpose in the above variable.
#NOte that for scientific work use TEMP_ADJUSTED, SAL_ADJUSTED, PRES_ADJUSTED.

date10 = dt.datetime(1950,1,1)


#print date10
#print timeargo.size
# A for loop is used below so that you can also cyclonic eddy data. Right now only anticyclonic eddy data used.
for ofilename in ['LB-anti-cycloniceddies2016.nc']:
    
    ds2 = Dataset(ofilename)
    y2 = ds2['year'][:]
    m2 = ds2['month'][:]
    d2 = ds2['day'][:]

    

    timeeddy = np.array([(dt.datetime(yy, mm, dd) - date10).days for yy,mm,dd in zip(y2.astype(int),
                                                                                     m2.astype(int),
                                                                                     d2.astype(int))], dtype=float)
    loneddy = ds2['lon'][:]
    lateddy = ds2['lat'][:]
    radeddy = ds2['Radius'][:]
    #ideddy = ds2['ID'][:]
    #print(timeargo.shape[0])

    for ii in range(0, timeargo.shape[0]):
        timeindx = np.where(timeargo[ii] == timeeddy)[0]
        loneddyN=loneddy[timeindx]
        lateddyN=lateddy[timeindx]
        radeddyN=radeddy[timeindx]
        
        #print timeindx
        #print(timeindx.shape[0])
        #print lateddyN

        # number of argo positions by number of eddies
        lat_argo_res = np.zeros((len(latargo), len(lateddyN))).T + latargo
        lon_argo_res = np.zeros((len(lonargo), len(loneddyN))).T + lonargo
        lat_eddy_res = np.zeros((len(latargo), len(lateddyN))) + lateddyN
        lon_eddy_res = np.zeros((len(lonargo), len(loneddyN))) + loneddyN

        
        # res: "reshaped"
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

        # distances in km between eddy centres and argo floats
        a = np.sin(dlat / 2)**2 + np.cos(lateddy_rad) * np.cos(latargo_rad) * np.sin(dlon / 2)**2
        c2 = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c2

        # distance in km, note eddy radius in meter.

        radeddyN=radeddyN/1000

        # Finding whether the Argo float is whithin an eddy. For that the distance between the eddy center and argo float center ....
        # ...should be less than one.
        # dist_min_rad=distance.T - radeddyN
        radeddyN_res = np.zeros((len(latargo), len(lateddyN))) + radeddyN
        mask = distance < radeddyN_res.T
        ids = np.where(mask)

        #print(ids)
        
        #this id wll give you the index of the Argo float, for e.g., in this case its 59.
        # e.g., The data you should plot is tempargo[59,:]

        #import ipdb; ipdb.set_trace()
