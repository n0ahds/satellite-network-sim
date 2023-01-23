ISS_TLE = """1 25544U 98067A   16341.96974289  .00003303  00000-0  57769-4 0  9996
2 25544  51.6456 276.4739 0005937 300.1004 104.8148 15.53811586 31866"""
L1, L2 = ISS_TLE.splitlines()

import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import Loader, EarthSatellite, Topos

degs     = 180./np.pi

r_earth  = 6371.  # for ROUGH approx. ground track, just use a spherical Earth

load    = Loader('~/Documents/YourNameHere/SkyData')
data    = load('de421.bsp')
earth   = data['earth']
topoZZ  = Topos(latitude_degrees=0.0, longitude_degrees=0.0)

location = earth + topoZZ

ISS      = earth + EarthSatellite(L1, L2)

ts       = load.timescale()

minutes  = np.arange(0, 140, 0.5)
time     = ts.utc(2016, 12, 7, 12, minutes)

Epos     = earth.at(time).position.km
ZZpos    = topoZZ.at(time).position.km    ## Position of (0.0N, 0.0E) to get rotation
ISSpos   = ISS.at(time).position.km - Epos

theta_ZZ = np.arctan2(ZZpos[1], ZZpos[0])   # calculate Earth's rotaion

sth, cth         = np.sin(-theta_ZZ), np.cos(-theta_ZZ) # unwind
xISS, yISS, zISS = ISSpos
xISSnew, yISSnew = xISS*cth - yISS*sth, xISS*sth + yISS*cth # rotate ISS data to match Earth
ISSnew           = np.vstack((xISSnew, yISSnew, zISS))

x, y, z = ISSnew
r       = np.sqrt((ISSpos**2).sum(axis=0))
rxy     = np.sqrt(x**2 + y**2)
ISSlat, ISSlon   = np.arctan2(z, rxy), np.arctan2(y, x)

plt.figure()
plt.plot(degs*ISSlon, degs*ISSlat, 'ok')
plt.show()
print('test')