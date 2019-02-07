import netCDF4
import numpy as np
import datetime
#import numpy.ma as ma

url = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/aoml/7900685/profiles/R7900685_002.nc'
#url = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/csiro/7900629/profiles/R7900629_003.nc'
#url = 'http://tds0.ifremer.fr/thredds/dodsC/CORIOLIS-ARGO-GDAC-OBS/nmdis/2901633/profiles/R2901633_071.nc'
nc = netCDF4.Dataset(url)
print nc.variables
print nc.variables.keys()
print nc.dimensions
# Time variable read
time    = nc.variables['JULD']

#Reading depth variable
depth = nc.variables['PRES']
print depth.shape

# checking whether there is more than one profile data on the same day
# if there is, then delete the wrong data, In here the sallowest profile is removed
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


print 'maxdepth', findepth[dd]
print 'checkdepth ',checkdepth
# Reading info about the data center
dc = nc.variables['DATA_CENTRE'][:]
dcstr2= ''.join(map(str, dc))
DataCenter = dcstr2.replace("--", "")

# Reading Platform number
platnum = nc.variables['PLATFORM_NUMBER'][0]
str2= ''.join(map(str, platnum))
platnumnew = str2.replace("--", "")

print 'platnumnew',platnumnew

datamodef = nc.variables['DATA_MODE'][dd]

if (datamodef == 'R'):
	
	datamode = 'Real time mode'
	print datamode

if (datamodef == 'A'):
	datamode = 'Delayed time mode'
	print datamode

# here are the final variables
MaxDepth = findepth[dd]
NewDate = datetime.datetime(1950, 1, 1, 0, 0) + datetime.timedelta(time[dd])
YearArgo = NewDate.strftime('%Y')
MonArgo = NewDate.strftime('%m')
DayArgo = NewDate.strftime('%d')

LatArgo = nc.variables['LATITUDE'][dd]
LonArgo = nc.variables['LONGITUDE'][dd]

print MaxDepth
print NewDate
print YearArgo
print MonArgo
print DayArgo
print LatArgo
print LonArgo
#print nc.comment
