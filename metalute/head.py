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
from metalute.matplotlib_ import plt
from metalute.geometry import Point, Line, CircularArc, Hole, ParametricPolyPathBase
from metalute.dimension import dim, vdim


class FenderStratocasterContour(ParametricPolyPathBase):

    """Contour for the Fender Stratocaster headstock.
    """

    DEFAULT_PAR_DICT = {'w': inches_to_mm(1.650),
                        'd1': 8.06,
                        'r1': 15.23,
                        'span1': 70.0,
                        'r2': 7.20,
                        'span2': 87.0,
                        'd2': 143.00,
                        'r3': 25.50,
                        'span3': 233.0,
                        'r4': 8.45,
                        'span4': 77.5,
                        'r5': 280.40,
                        'span5': 8.0,
                        'r6': 169.60,
                        'span6': 13.2,
                        'r7': 50.50
                        }

    def construct(self):
        """Overloaded method.
        """
        p1 = self.anchor.vmove(0.5 * self.w)
        p2 = p1.hmove(self.d1)
        line1 = Line(p1, p2)
        arc1 = line1.connecting_circular_arc(self.r1, self.span1)
        arc2 = arc1.connecting_circular_arc(-self.r2, self.span2)
        line2 = arc2.connecting_line(self.d2)
        arc3 = line2.connecting_circular_arc(-self.r3, -self.span3)
        arc4 = arc3.connecting_circular_arc(self.r4, -self.span4)
        arc5 = arc4.connecting_circular_arc(self.r5, self.span5)
        arc6 = arc5.connecting_circular_arc(-self.r6, self.span6)
        # Last circle---here things are a little bit tricky :-)
        p = arc6.end_point()
        phi = np.degrees(np.arccos(1. - (-0.5 * self.w - p.y) / self.r7))
        dx = self.r7 * np.sin(np.radians(phi))
        c7 = Point(p.x - dx, -0.5 * self.w - self.r7)
        arc7 = CircularArc(c7, self.r7, 90. - phi, phi)
        line3 = arc7.connecting_line(arc7.end_point().x)
        return locals()



class FenderStratocaster:

    """
    """

    def __init__(self, **kwargs):
        """
        """
        self.contour = FenderStratocasterContour()

    def draw(self, offset, **kwargs):
        """
        """
        hole_distance_to_edge = 11.35
        hole_diameter = 10.
        string_pitch = 7.15
        g_string_offset = 1.15
        self.contour.draw(offset, **kwargs)
        slope = self.contour.path('line2').slope()
        arc = self.contour.path('arc2')
        pivot = arc.end_point().move(hole_distance_to_edge, arc.end_phi - 180.)
        scale = 1. / abs(np.sin(np.radians(slope)))
        pitch = string_pitch * scale
        delta = (pivot.y + g_string_offset) * scale - 3. * pitch
        for i in range(6):
            p = pivot.move(i * pitch + delta, slope)
            Hole(p, hole_diameter).draw(offset, **kwargs)

    def dimension_top(self, offset):
        """
        """
        #dim(self.point('p1'), self.point('p11'), offset)
        #dim(self.hole(1).center, self.hole(0).center, offset)
        #vdim(self.hole(5).center, self.hole(4).center, offset, distance=30.)
        #vdim(self.point('p4'), self.point('p9'), offset)
        pass
