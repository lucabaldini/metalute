# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Luca Baldini (luca.baldini@pi.infn.it)
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

"""Fitting-related facilities.
"""

import numpy as np
from scipy.interpolate import splprep, splev
from scipy.optimize import curve_fit, leastsq

from metalute.geometry import Point, Circle


def distance_from_center(x, y, x0, y0):
    """
    """
    return np.sqrt((x - x0)**2. + (y - y0)**2.)


def circle_residuals(center, x, y):
    """
    """
    r = distance_from_center(x, y, *center)
    return r - r.mean()


def fit_circle(x, y):
    """
    """
    barycenter = np.mean(x), np.mean(y)
    center, _ = leastsq(circle_residuals, barycenter, args=(x,y))
    radius = distance_from_center(x, y, *center).mean()
    return Point(*center), radius



"""
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
    return np.sqrt((x-xc)**2 + (y-yc)**2)

def f(c, x, y):
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
"""
