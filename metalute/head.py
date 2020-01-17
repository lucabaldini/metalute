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
from metalute.geometry import Point, Line, PolyLine, CircularArc, Hole, ParametricPolyPathBase
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
        self.countour = FenderStratocasterContour()

    def draw(self, offset, **kwargs):
        """
        """
        hole_distance_to_edge = 11.35
        hole_diameter = 10.
        string_pitch = 7.15
        g_string_offset = 1.15

        self.countour.draw(offset, **kwargs)
        #phi = self.phi1 - self.phi2
        #pivot = p4.move(hole_distance_to_edge, arc2.phi1 - 180., 'pivot')
        #scale = 1. / abs(np.sin(np.radians(phi)))
        #pitch = string_pitch * scale
        #offset = (pivot.y + g_string_offset) * scale - 3. * pitch
        #for i in range(6):
        #    _p = pivot.move(i * pitch + offset, phi)
        #    h = Hole(_p, hole_diameter, 'h{}'.format(i + 1))
        #    self.add_holes(h)




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
        self.anchor = Point(0., 0., 'anchor')
        self.point_dict = {}
        self.patch_dict = {}
        self.hole_list = []
        self.construct()

    def __getattr__(self, key):
        """Remove me---it makes debug harder.
        """
        return self.params[key]

    def add_points(self, *points):
        """
        """
        for point in points:
            if point.name is not None:
                self.point_dict[point.name] = point

    def point(self, name):
        """
        """
        return self.point_dict[name]

    def hole(self, i):
        """
        """
        return self.hole_list[i]

    def add_patches(self, *patches):
        """
        """
        for patch in patches:
            if patch.name is not None:
                self.patch_dict[patch.name] = patch

    def add_holes(self, *holes):
        """
        """
        self.hole_list += holes

    def construct(self):
        """
        """
        raise NotImplementedError

    def draw_top_axis(self, offset, padding: float = 10.):
        """
        """
        p0 = self.anchor.move(padding, 180.)
        p1 = self.anchor.move(200., 0.) #Fixme
        PolyLine(p0, p1).draw(offset, ls='dashdot')

    def draw_top(self, offset, points: bool=False, construction: bool=False):
        """
        """
        self.draw_top_axis(offset)
        for patch in self.patch_dict.values():
            if isinstance(patch, CircularArc):
                patch.draw(offset, full_circle=construction, radii=construction)
            else:
                patch.draw(offset)
        for hole in self.hole_list:
            hole.draw(offset)
        if points:
            for point in self.point_dict.values():
                point.draw(offset)



class StratoHeadstock(Headstock):

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
                      'r7': 50.50
                      }

    def construct(self):
        """Overloaded method.
        """
        # Starting horizontal segment.
        p1 = self.anchor.move(0.5 * self.w, 90., 'p1')
        p2 = p1.move(self.d1, 0., 'p2')
        line1 = PolyLine(p1, p2, name='line1')
        # First circle.
        c1 = p2.move(self.r1, 90., 'c1')
        arc1 = CircularArc(c1, self.r1, -90., self.phi1 - 90., 'arc1')
        p3 = arc1.end_point('p3')
        # Second circle.
        c2 = p3.move(self.r2, arc1.phi2, 'c2')
        arc2 = CircularArc(c2, self.r2, 90 + self.phi1 - self.phi2, 90. + self.phi1, 'arc2')
        p4 = arc2.start_point('p4')
        # Long straight segment.
        p5 = p4.move(self.d2, arc2.phi1 - 90., 'p5')
        line2 = PolyLine(p4, p5, name='line2')
        # Third circle.
        c3 = p5.move(self.r3, arc2.phi1 - 180., 'c3')
        arc3 = CircularArc(c3, self.r3, arc2.phi1 - self.phi3, arc2.phi1, 'arc3')
        p6 = arc3.start_point('p6')
        # Fourth circle.
        c4 = p6.move(self.r4, arc3.phi1, 'c4')
        arc4 = CircularArc(c4, self.r4, 180. + arc3.phi1, 180. + arc3.phi1 + self.phi4, 'arc4')
        p7 = arc4.end_point('p7')
        # Fifth circle.
        c5 = p7.move(self.r5, arc4.phi2 + 180., 'c5')
        arc5 = CircularArc(c5, self.r5, arc4.phi2, arc4.phi2 + self.phi5, 'arc5')
        p8 = arc5.end_point('p8')
        # Sixth circle.
        c6 = p8.move(self.r6, arc5.phi2, 'c6')
        arc6 = CircularArc(c6, self.r6, 180. + arc5.phi2 - self.phi6, 180. + arc5.phi2, 'arc6')
        p9 = arc6.start_point('p9')
        # Last circle---here things are a little bit tricky :-)
        phi = np.degrees(np.arccos(1. - (-0.5 * self.w - p9.y) / self.r7))
        dx = self.r7 * np.sin(np.radians(phi))
        c7 = Point(p9.x - dx, -0.5 * self.w - self.r7, 'c7')
        arc7 = CircularArc(c7, self.r7, 90. - phi, 90., 'arc7')
        p10 = arc7.end_point('p10')
        # And finally: close the loop.
        p11 = self.anchor.move(0.5 * self.w, -90., 'p11')
        line3 = PolyLine(p11, p10, name='line3')
        # Add all the points and patches to the headstock.
        self.add_points(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11)
        self.add_patches(line1, line2, line3)
        self.add_patches(arc1, arc2, arc3, arc4, arc5, arc6, arc7)

        # Now the holes.
        hole_distance_to_edge = 11.35
        hole_diameter = 10.
        string_pitch = 7.15
        g_string_offset = 1.15
        phi = self.phi1 - self.phi2

        pivot = p4.move(hole_distance_to_edge, arc2.phi1 - 180., 'pivot')
        scale = 1. / abs(np.sin(np.radians(phi)))
        pitch = string_pitch * scale
        offset = (pivot.y + g_string_offset) * scale - 3. * pitch
        for i in range(6):
            _p = pivot.move(i * pitch + offset, phi)
            h = Hole(_p, hole_diameter, 'h{}'.format(i + 1))
            self.add_holes(h)

    def dimension_top(self, offset):
        """
        """
        dim(self.point('p1'), self.point('p11'), offset)
        dim(self.hole(1).center, self.hole(0).center, offset)
        vdim(self.hole(5).center, self.hole(4).center, offset, distance=30.)
        #vdim(self.point('p4'), self.point('p9'), offset)
