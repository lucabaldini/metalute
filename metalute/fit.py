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

from metalute.geometry import Point, Line, CircularArc


def distance_from_center(x, y, x0, y0):
    """
    """
    return np.sqrt((x - x0)**2. + (y - y0)**2.)


def circle_residuals(center, x, y):
    """
    """
    r = distance_from_center(x, y, *center)
    return r - r.mean()


def fit_circle_arc(x, y, imin: int = 0, imax: int = -1, invert: bool = False):
    """
    """
    x = x[imin:imax + 1]
    y = y[imin:imax + 1]
    barycenter = np.mean(x), np.mean(y)
    center, _ = leastsq(circle_residuals, barycenter, args=(x,y))
    radius = distance_from_center(x, y, *center).mean()
    center = Point(*center)
    phi1 = Line(center, Point(x[0], y[0])).slope()
    phi2 = Line(center, Point(x[-1], y[-1])).slope()
    if invert:
        phi1, phi2 = phi2, phi1
    arc = CircularArc(center, radius, phi1, phi2)
    print(arc)
    return arc



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

"""
