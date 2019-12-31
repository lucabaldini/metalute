# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Headstock-related facilities.
"""

# We have to sort this out---the default is not working on my Fedora 30.
import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from scipy.optimize import curve_fit, leastsq

from metalute.units import inches_to_mm

DATA = """
120.11551155115512, 46.41914191419142
126.81518151815182, 46.41914191419142
136.86468646864688, 46.41914191419142
143.56435643564356, 46.41914191419142
153.6138613861386, 43.54785478547855
161.74917491749176, 37.32673267326733
166.05610561056105, 30.627062706270628
170.36303630363037, 22.97029702970297
175.14851485148515, 16.74917491749175
181.84818481848185, 13.877887788778878
188.06930693069307, 14.834983498349835
204.33993399339934, 19.141914191419144
217.73927392739273, 23.448844884488448
270.8580858085809, 39.71947194719472
332.5907590759076, 58.382838283828384
386.18811881188117, 75.13201320132013
419.6864686468647, 85.66006600660066
467.54125412541254, 100.01650165016501
486.6831683168317, 105.75907590759076
499.12541254125415, 110.06600660066007
512.5247524752475, 119.63696369636963
522.0957095709571, 132.07920792079207
528.7953795379537, 147.3927392739274
529.2739273927393, 168.44884488448847
525.4455445544554, 182.8052805280528
516.8316831683169, 196.20462046204622
502.4752475247525, 208.64686468646866
486.6831683168317, 214.3894389438944
474.71947194719473, 216.30363036303632
457.970297029703, 213.91089108910893
444.0924092409241, 208.16831683168317
432.60726072607264, 198.5973597359736
424.950495049505, 187.59075907590758
419.6864686468647, 178.97689768976898
415.8580858085809, 172.75577557755776
408.6798679867987, 167.97029702970298
393.8448844884488, 168.44884488448847
374.7029702970297, 171.32013201320132
346.94719471947195, 176.58415841584159
319.1914191419142, 183.76237623762376
278.51485148514854, 192.85478547854785
249.8019801980198, 196.68316831683168
233.05280528052805, 197.64026402640263
223.003300330033, 184.24092409240924
212.95379537953795, 173.23432343234325
199.55445544554456, 161.27062706270627
180.8910891089109, 149.78547854785478
164.62046204620464, 141.65016501650166
148.34983498349834, 139.73597359735973
134.95049504950495, 138.77887788778878
127.29372937293729, 138.77887788778878
120.5940594059406, 139.25742574257427
"""

HOLES = """
212.4752475247525, 47.85478547854785
264.15841584158414, 63.646864686468646
315.3630363036304, 79.91749174917491
367.5247524752475, 95.23102310231023
418.72937293729376, 111.02310231023102
470.4125412541254, 126.81518151815182
"""


plt.figure()
plt.gca().set_aspect('equal')
x = []
y = []
for line in DATA.split('\n'):
    try:
        _x, _y = [float(item) for item in line.split(',')]
        x.append(_x)
        y.append(_y)
    except:
        pass
x = np.array(x)
x -= x.min()
scale = x.max() / inches_to_mm(7.313)
print(scale)
x /= scale
y = np.array(y)
y /= -scale
y -= 0.5 * (y[0] + y[-1])
plt.plot(x, y, 'o')

pts = np.vstack((x, y))

tck, u = splprep(pts, u=None, s=0.0)#, per=1)
u_new = np.linspace(u.min(), u.max(), 1000)
x_new, y_new = splev(u_new, tck, der=0)
#plt.plot(x_new, y_new)

def line(x, m, q):
    return m * x + q

def const(x, q):
    return np.full(x.shape, q)

def calc_R(x, y, xc, yc):
    """ calculate the distance of each 2D points from the center (xc, yc) """
    return np.sqrt((x-xc)**2 + (y-yc)**2)

def f(c, x, y):
    """ calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc) """
    Ri = calc_R(x, y, *c)
    return Ri - Ri.mean()

def leastsq_circle(x,y):
    # coordinates of the barycenter
    x_m = np.mean(x)
    y_m = np.mean(y)
    center_estimate = x_m, y_m
    center, ier = leastsq(f, center_estimate, args=(x,y))
    xc, yc = center
    Ri       = calc_R(x, y, *center)
    R        = Ri.mean()
    return xc, yc, R

_x = x[:3]
_y = y[:3]
popt, pcov = curve_fit(const, _x, _y)
print(popt)
_x = np.linspace(0, 20, 100)
plt.plot(_x, const(_x, *popt))

_x = x[3:8]
_y = y[3:8]
x0, y0, r = leastsq_circle(_x, _y)
print(x0, y0, r)
circle = plt.Circle((x0, y0), radius=r, fill=False)
plt.gca().add_patch(circle)

_x = x[7:10]
_y = y[7:10]
x0, y0, r = leastsq_circle(_x, _y)
print(x0, y0, r)
circle = plt.Circle((x0, y0), radius=r, fill=False)
plt.gca().add_patch(circle)

_x = x[11:18]
_y = y[11:18]
#plt.plot(_x, _y, 'o')
popt, pcov = curve_fit(line, _x, _y)
_x = np.linspace(0, 200, 100)
plt.plot(_x, line(_x, *popt))

_x = x[19:32]
_y = y[19:32]
x0, y0, r = leastsq_circle(_x, _y)
print(x0, y0, r)
circle = plt.Circle((x0, y0), radius=r, fill=False)
plt.gca().add_patch(circle)
#arc = matplotlib.patches.Arc((x0, y0), 2. * r, 2. * r, 0., -120., 80., fill=False)
#plt.gca().add_patch(arc)

_x = x[33:36]
_y = y[33:36]
x0, y0, r = leastsq_circle(_x, _y)
print(x0, y0, r)
circle = plt.Circle((x0, y0), radius=r, fill=False)
plt.gca().add_patch(circle)

_x = x[36:39]
_y = y[36:39]
x0, y0, r = leastsq_circle(_x, _y)
print(x0, y0, r)
circle = plt.Circle((x0, y0), radius=r, fill=False)
plt.gca().add_patch(circle)

_x = x[39:43]
_y = y[39:43]
x0, y0, r = leastsq_circle(_x, _y)
print(x0, y0, r)
circle = plt.Circle((x0, y0), radius=r, fill=False)
plt.gca().add_patch(circle)

_x = x[43:53]
_y = y[43:53]
x0, y0, r = leastsq_circle(_x, _y)
print(x0, y0, r)
circle = plt.Circle((x0, y0), radius=r, fill=False)
plt.gca().add_patch(circle)

_x = x[-3:]
_y = y[-3:]
popt, pcov = curve_fit(const, _x, _y)
print(popt)
_x = np.linspace(0, 20, 100)
plt.plot(_x, const(_x, *popt))

plt.axis([0, 200, -60, 60])
plt.show()
