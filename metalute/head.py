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


import numpy as np
#from scipy.interpolate import splprep, splev
#from scipy.optimize import curve_fit, leastsq

from metalute.units import inches_to_mm
from metalute.matplotlib_ import plt, drafting_figure
from metalute.geometry import Point, PolyLine, CircleArc, circle, circle_arc, circle_arc_construction

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


class Headstock:

    """Class representing a guitar headstokes.
    """

    DEFAULT_PARAMS = {}

    def __init__(self, **kwargs):
        """Constructor.
        """
        # mind this is a shallow copy.    print(matplotlib.rcParams.keys())

        self.params = self.DEFAULT_PARAMS.copy()
        self.params.update(**kwargs)
        self.points = []
        self.patches = []
        self.construct()

    def __getattr__(self, key):
        """
        """
        return self.params[key]

    def add_points(self, *points):
        """
        """
        self.points += points

    def add_patches(self, *patches):
        """
        """
        self.patches += patches

    def construct(self):
        """
        """
        raise NotImplementedError

    def draw_top(self, offset):
        """
        """
        for patch in self.patches:
            patch.draw(offset)
        for point in self.points:
            point.draw(offset)



class FenderHeadstock(Headstock):

    """
    """

    DEFAULT_PARAMS = {'w': inches_to_mm(1.650),
                      'd1': 8.06,
                      'r1': 15.23,
                      'phi1': 70.0,
                      'r2': 7.20,
                      'phi2': 87.0,
                      'd2': 143.00,
                      'r3': 25.50,
                      'phi3': 233.0,
                      'r4': 8.45,
                      'phi4': 62.5
                      }

    def construct(self):
        """
        """
        # Anchor---this is on the neck axis, at the mid point of the nut.
        anchor = Point(0., 0., 'anchor')
        p1 = anchor.move(0.5 * self.w, 90., 'p1')
        p2 = p1.move(self.d1, 0., 'p2')
        line1 = PolyLine(p1, p2)
        c1 = p2.move(self.r1, 90., 'c1')
        phi1 = -90.
        phi2 = self.phi1 - 90.
        arc1 = CircleArc(c1, self.r1, phi1, phi2)
        p3 = c1.move(self.r1, phi2, 'p3')
        c2 = p3.move(self.r2, phi2, 'c2')
        phi1 = 90 + self.phi1 - self.phi2
        phi2 = 90. + self.phi1
        arc2 = CircleArc(c2, self.r2, phi1, phi2)
        p4 = c2.move(self.r2, phi1, 'p4')
        p5 = p4.move(self.d2, phi1 - 90., 'p5')
        line2 = PolyLine(p4, p5)
        c3 = p5.move(self.r3, phi1 - 180., 'c3')
        phi2 = phi1
        phi1 = phi1 - self.phi3
        arc3 = CircleArc(c3, self.r3, phi1, phi2)
        p6 = c3.move(self.r3, phi1, 'p6')
        c4 = p6.move(self.r4, phi1, 'c4')
        phi1 = 180. + phi1
        phi2 = phi1 + self.phi4
        arc4 = CircleArc(c4, self.r4, phi1, phi2)
        p7 = c4.move(self.r4, phi2, 'p7')

        # Add all the points and patches to the headstock.
        self.add_points(p1, p2, p3, p4, p5, p6, p7)
        self.add_points(anchor, c1, c2, c3, c4)
        self.add_patches(line1, arc1, arc2, line2, arc3, arc4)





drafting_figure('Fender headstock', 'A4')
headstock = FenderHeadstock()
offset = Point(-90., 10.)
headstock.draw_top(offset)



w = inches_to_mm(1.650)
d1 = 8.06
r1 = 15.23
phi1 = 20.0
r2 = 7.20
phi2 = 17.0
d2 = 143.00
r3 = 25.50
phi3 = 70.0
r4 = 8.45
phi4 = 7.5
r5 = 280.40
phi5 = 15.5
r6 = 169.60
phi6 = 2.3 # This is not independent from phi7
r7 = 50.50
d3 = 6.00
phi7 = 27.5 # This should be calculated

offset = Point(0., 0.)

plt.figure()
plt.gca().set_aspect('equal')
p1 = Point(0., 0.5 * w, 'p1')
p2 = Point(d1, 0.5 * w, 'p2')
p1.draw(offset)
p2.draw(offset, va='top')


plt.hlines(0.5 * w, 0., d1)
#
x0 = d1
y0 = r1 + 0.5 * w
circle_arc((x0, y0), r1, -90., -phi1, construction=True)
#
x0 += (r1 + r2) * np.cos(np.radians(phi1))
y0 -= (r1 + r2) * np.sin(np.radians(phi1))
circle_arc((x0, y0), r2, 90. - phi2, 180. - phi1, construction=True)
#
x0 += r2 * np.sin(np.radians(phi2))
y0 += r2 * np.cos(np.radians(phi2))
x1 = x0 + d2 * np.cos(np.radians(phi2))
y1 = y0 - d2 * np.sin(np.radians(phi2))
plt.plot([x0, x1], [y0, y1], color='black', lw=1.)
#
x0 = x1 - r3 * np.sin(np.radians(phi2))
y0 = y1 - r3 * np.cos(np.radians(phi2))
circle_arc((x0, y0), r3, -90. - phi3, 90. - phi2, construction=True)
#
x0 -= (r3 + r4) * np.sin(np.radians(phi3))
y0 -= (r3 + r4) * np.cos(np.radians(phi3))
circle_arc((x0, y0), r4, 90. - phi3, 90. + phi4, construction=True)
#
x0 += (-r4 + r5) * np.sin(np.radians(phi4))
y0 -= (-r4 + r5) * np.cos(np.radians(phi4))
circle_arc((x0, y0), r5, 90. + phi4, 90. + phi5, construction=True)
#
x0 -= (r5 + r6) * np.sin(np.radians(phi5))
y0 += (r5 + r6) * np.cos(np.radians(phi5))
circle_arc((x0, y0), r6, -90. + phi6, -90. + phi5, construction=True)
#
x0 = d3
y0 = -0.5 * w - r7
circle_arc((x0, y0), r7, phi7, 90., construction=True)
#
plt.hlines(-0.5 * w, 0., d3)

plt.show()
