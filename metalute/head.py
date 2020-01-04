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

from metalute.units import inches_to_mm
from metalute.matplotlib_ import plt, drafting_figure
from metalute.geometry import Point, PolyLine, CircleArc, circle, circle_arc, circle_arc_construction



class Headstock:

    """Class representing a guitar headstokes.
    """

    DEFAULT_PARAMS = {}

    def __init__(self, **kwargs):
        """Constructor.
        """
        # Mind this is a shallow copy.
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

    def draw_top(self, offset, points: bool=False, construction: bool=False):
        """
        """
        for patch in self.patches:
            if isinstance(patch, CircleArc):
                patch.draw(offset, full_circle=construction, radii=construction)
            else:
                patch.draw(offset)
        if points:
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
                      'phi4': 77.5,
                      'r5': 280.40,
                      'phi5': 8.0,
                      'r6': 169.60,
                      'phi6': 13.2,
                      'r7': 50.50,
                      'd3': 6.00
                      }

    def construct(self):
        """Overloaded method.
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
        c5 = p7.move(self.r5, phi2 + 180., 'c5')
        phi1 = phi2
        phi2 = phi1 + self.phi5
        arc5 = CircleArc(c5, self.r5, phi1, phi2)
        p8 = c5.move(self.r5, phi2, 'p8')
        c6 = p8.move(self.r6, phi2, 'c6')
        phi1 = 180. + phi2 - self.phi6
        phi2 = 180. + phi2
        arc6 = CircleArc(c6, self.r6, phi1, phi2)
        p9 = c6.move(self.r6, phi1, 'p9')

        p11 = anchor.move(0.5 * self.w, -90., 'p11')
        p10 = p11.move(self.d3, 0., 'p10')
        line3 = PolyLine(p11, p10)
        c7 = p10.move(self.r7, -90, 'c7')
        dx, dy = (p9 - c7).xy()
        phi1 = np.degrees(np.arctan2(dy, dx))
        phi2 = 90.
        arc7 = CircleArc(c7, self.r7, phi1, phi2)

        # Add all the points and patches to the headstock.
        self.add_points(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11)
        self.add_patches(line1, line2, line3)
        self.add_patches(arc1, arc2, arc3, arc4, arc5, arc6, arc7)
