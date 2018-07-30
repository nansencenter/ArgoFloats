import sys
import netCDF4
import numpy as np
import datetime

from decimal import getcontext, Decimal




#url = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/aoml/7900685/7900685_Rtraj.nc'

url='http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/aoml/15851/15851_Rtraj.nc'
nc = netCDF4.Dataset(url)

timefirst = nc.variables['JULD_FIRST_LOCATION']
print timefirst[:]
time = np.delete(timefirst,'--')

print time



yrall = np.zeros(time.shape[0])
monall = np.zeros(time.shape[0])
dayall = np.zeros(time.shape[0])

print time.shape[0]
for k in range (0, time.shape[0]):
	a = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[k])
	yrall[k] = a.strftime('%Y')
	monall[k] = a.strftime('%m')
	dayall[k] = a.strftime('%d')
	print a
	print k


platnum = nc.variables['PLATFORM_NUMBER'][dd]

#str1 = ''.join(str(v) for v in platnum)

str2= ''.join(map(str, platnum))
platnumnew = str2.replace("--", "")
#print len(platnum)

platfin = np.zeros(time.shape[0])
for pp in range(time.shape[0]):
	platfin[pp]=platnumnew



lat = nc.variables['LATITUDE'][:]
newlat = np.extract(abs(lat) > 0, lat)
extlat = np.around(newlat, 1)
finlat = extlat[::2]


lon = nc.variables['LONGITUDE'][:]
newlon = np.extract(abs(lon) > 0, lon)
extlon = np.around(newlon, 1)
finlon = extlon[::2]


if (finlon.shape[0] != time.shape[0]):
        print 'Size of longitude metatdata: ',finlon.shape[0]
        print 'Size of time metatdata: ',time.shape[0]
        sys.exit('Error : Something went wrong when reading the longitude metadata')
        
if (finlat.shape[0] != time.shape[0]):
        print 'Size of latitude metatdata: ',finlat.shape[0]
        print 'Size of time metatdata: ',time.shape[0]
	sys.exit('Error : Something went wrong when reading the latitude metadata')

dc = nc.variables['DATA_CENTRE'][:]
dcstr2= ''.join(map(str, dc))
DataCenter = dcstr2.replace("--", "")



print DataCenter
print yrall
print monall
print dayall



print platnum
print platnumnew
print platfin



print lat
print platfin
print extlat
print finlat
print finlon
print nc.summary
#print extlon

#JULD_ASCENT_END

#print time[0]
#nc    = Dataset("/home/vagrant/geospaas_project/argo_floats/data/R7900685_010.nc")

#time    = nc.variables['JULD'][0]
#platnum = nc.variables['PLATFORM_NUMBER'][0]

#print ''.join(str(platnum))
#a = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[j])
#newdate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time)

#Temp = nc.variables['TEMP'][0]
#Pres = nc.variables['PRES'][0]
#Sal = nc.variables['PSAL'][0]

#TempAdj = nc.variables['TEMP_ADJUSTED'][0]
#PresAdj = nc.variables['PRES_ADJUSTED'][0]
#SalAdj = nc.variables['PSAL_ADJUSTED'][0]

#Lat = nc.variables['LATITUDE'][0]
#Lon = nc.variables['LONGITUDE'][0]
#datamodef = nc.variables['DATA_MODE'][0]

#if (datamodef == 'R'):
#	TempFin = Temp
#	PresFin = Pres
#	SalFin = Sal

#if (datamodef == 'A'):
#	TempFin = TempAdj
#	PresFin = PresAdj
#	SalFin = SalAdj

#print time
#print newdate
#print Lat
#print Lon
#print len(Temp)
#print len(Pres)
#print Temp[0:10]
#print TempFin[0:10]
#print Sal[0:10]
#print SalFin[0:10]
#print Pres[0:10]
#print PresFin[0:10]
#print datamodef
