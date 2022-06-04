#! /usr/bin/env python
#
#   Example reducing SEQ/Bs spectra using pyspeckit
#   using data from 2021-S1-UM-3
#

import sys
import numpy as np
import matplotlib.pyplot as plt
import pyspeckit
from astropy.io import fits
import astropy.units as u

#
src = 'UGCA281'

#  list of osbnums
on = [100536, 100538, 100540, 100544, 100546, 100548, 100550, 100554, 100556, 100558]

#  range to analyse
xmin=-200 * u.km/u.s
xmax= 700 * u.km/u.s

#  section to ignore for baseline fitting, presumably where galaxy is expected
bmin= 200 * u.km/u.s
bmax= 350 * u.km/u.s

#  final binning (in pixels)
vbin = 5.5

#  show individual spectra?
Qshow = False

#  build up spectra from each obsnum, baseline and resample them
s  = []
for o in on:
    #  pyspeckit should be able to read a spectrum directly if the tabfile is made smarter
    tabfile = '%s_%d.txt' % (src,o)
    data = np.loadtxt(tabfile).T
    x = data[0]
    y = data[1] * 1000
    n = len(x)
    sp = pyspeckit.Spectrum(data=y, xarr=x,
                           xarrkwargs={'unit':'km/s'},
                           unit='mK')
    sp.baseline.selectregion(xmin=xmin,xmax=xmax, exclude=[bmin,bmax])
    sp.baseline(order=1)
    sp.smooth(vbin, smoothtype='boxcar', downsample=True)
    s1 = sp.slice(xmin,xmax)
    
    s.append(s1)
    
    print("OBSNUM: ",o)
    print("Velocity axis:  %g .. %g  step %g km/s   %d channels" % (x[0], x[n-1], x[1]-x[0], n))
    print("Raw Data:   mean/rms/min/max: %g %g  %g %g" % (y.mean(), y.std(), y.min(), y.max()))

    if Qshow:
        print(s1.stats())
        fig = plt.figure()
        s1.plotter(fig)
        s1.specfit(components=True)
        plt.title("%d" % o)
        plt.show()

s2 = pyspeckit.ObsBlock(s)        
s3 = s2.average()
s3_stats = s3.stats()
print(s3_stats)
fig = plt.figure()
s3.plotter(fig)
s3.baseline(order=1,save=True,highlight_fitregion=True,exclude=[bmin,bmax],baseline_fit_color='blue')
s3.specfit()
plt.title("%s %d_%d   (rms=%g mK)" % (src,on[0],on[-1],s3_stats['std']))
plt.savefig("%s.png" % src)
plt.show()

