# -*- coding: utf-8 -*-
#
# Copyright (C) 2019--2020 Luca Baldini (luca.baldini@pi.infn.it)
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



class HeadstockContourBase(ParametricPolyPathBase):

    """Base class for headstocks contours.
    """

    def __init__(self, **kwargs):
        """Constructor.
        """
        super().__init__(**kwargs)
        assert 'width_at_nut' in self.par_dict.keys()



class HeadstockBase:

    """Base class for guitar headstocks.
    """

    CONTOUR_CLASS = None

    def __init__(self, hole_diameter: float = 10., thickness: float = 12.,
                 angle: float = 0., **kwargs):
        """Constructor.
        """
        self.contour = self.CONTOUR_CLASS(**kwargs)
        self.hole_diameter = hole_diameter
        self.thinckness = thickness
        self.angle = angle
        self.holes = []
        self.place_holes()

    def place_holes(self):
        """Do-nothing method to be reimplemented in derived classes.
        """
        raise NotImplementedError

    def add_hole(self, center):
        """Add a hole to the headstock.
        """
        self.holes.append(Hole(center, self.hole_diameter))

    def draw_top(self, offset, **kwargs):
        """Draw the top view.
        """
        # Draw the contour.
        self.contour.draw(offset, **kwargs)
        # Draw the holes.
        for hole in self.holes:
            hole.draw(offset, **kwargs)
        # Draw the axis.
        padding = 20.
        length = 150.
        p1 = self.contour.anchor.hmove(-padding)
        p2 = self.contour.anchor.hmove(length + padding)
        kwargs.setdefault('color', 'lightgrey')
        kwargs.setdefault('ls', 'dashdot')
        Line(p1, p2).draw(offset, **kwargs)


class FenderStratocasterContour(HeadstockContourBase):

    """Contour for the Fender Stratocaster headstock.
    """

    DEFAULT_PAR_DICT = {'width_at_nut': inches_to_mm(1.650),
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
        p1 = self.anchor.vmove(0.5 * self.width_at_nut)
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
        phi = np.degrees(np.arccos(1. - (-0.5 * self.width_at_nut - p.y) / self.r7))
        dx = self.r7 * np.sin(np.radians(phi))
        c7 = Point(p.x - dx, -0.5 * self.width_at_nut - self.r7)
        arc7 = CircularArc(c7, self.r7, 90. - phi, phi)
        line3 = arc7.connecting_line(arc7.end_point().x)
        return locals()



class FenderStratocaster(HeadstockBase):

    """The actual Fender Stratocaster headstock.
    """

    CONTOUR_CLASS = FenderStratocasterContour

    def place_holes(self):
        """
        """
        hole_distance_to_edge = 11.35
        string_pitch = 7.15
        g_string_offset = 1.15
        slope = self.contour.path('line2').slope()
        arc = self.contour.path('arc2')
        pivot = arc.end_point().move(hole_distance_to_edge, arc.end_phi - 180.)
        scale = 1. / abs(np.sin(np.radians(slope)))
        pitch = string_pitch * scale
        delta = (pivot.y + g_string_offset) * scale - 3. * pitch
        for i in range(6):
            self.add_hole(pivot.move(i * pitch + delta, slope))

    def dimension_top(self, offset):
        """
        """
        #dim(self.point('p1'), self.point('p11'), offset)
        #dim(self.hole(1).center, self.hole(0).center, offset)
        #vdim(self.hole(5).center, self.hole(4).center, offset, distance=30.)
        #vdim(self.point('p4'), self.point('p9'), offset)
        pass



class MusicManContour(HeadstockContourBase):

    """Contour for the typical Music Man headstock.
    """

    DEFAULT_PAR_DICT = {'width_at_nut': 41.30,
                        'd1': 4.00,
                        'r1': 15.00,
                        'span1': 50.00,
                        'd2': 13.00,
                        'r2': 5.00,
                        'span2': 65.25,
                        'd3': 98.50,
                        'r3': 23.00,
                        'span3': 173.00,
                        'r4': 20.14,
                        'phi4': -157.,
                        'span4': 86.00,
                        'd4': 20.,
                        'r5': 280.00,
                        'span5': 6.80,
                        'r6': 4.00,
                        'span6': 58.00,
                        'd5': 10.00
                        }

    def construct(self):
        """Overloaded method.
        """
        p1 = self.anchor.vmove(0.5 * self.width_at_nut)
        p2 = p1.hmove(self.d1)
        line1 = Line(p1, p2)
        arc1 = line1.connecting_circular_arc(self.r1, self.span1)
        line2 = arc1.connecting_line(self.d2)
        arc2 = line2.connecting_circular_arc(-self.r2, -self.span2)
        line3 = arc2.connecting_line(-self.d3)
        arc3 = line3.connecting_circular_arc(-self.r3, -self.span3)
        c4 = arc3.end_point().move(self.r4, self.phi4)
        arc4 = CircularArc(c4, self.r4, self.phi4 + 180., self.span4)
        line4 = arc4.connecting_line(self.d4)
        arc5 = line4.connecting_circular_arc(-self.r5, -self.span5)
        arc6 = arc5.connecting_circular_arc(-self.r6, -self.span6)
        line5 = arc6.connecting_line(self.d5)
        # Close the loop---again, a but tricky.
        span = 180. - line5.slope()
        r = (-0.5 * self.width_at_nut - line5.end_point().y) / (1. - np.cos(np.radians(span)))
        arc7 = line5.connecting_circular_arc(r, span)
        line6 = arc7.connecting_line(arc7.end_point().x)
        return locals()



class MusicMan(HeadstockBase):

    """The actual Music Man headstock.
    """

    CONTOUR_CLASS = MusicManContour

    def place_holes(self):
        """
        """
        hole_distance_to_edge = 12.634
        string_pitch = 6.7
        g_string_offset = -1.45
        slope = self.contour.path('line3').slope()
        arc = self.contour.path('arc2')
        pivot = arc.end_point().move(hole_distance_to_edge, arc.end_phi)
        scale = 1. / abs(np.sin(np.radians(slope)))
        pitch = string_pitch * scale
        delta = (pivot.y + g_string_offset) * scale - 3. * pitch
        for i in range(4):
            self.add_hole(pivot.move(i * pitch + delta, slope))
        # This is horrible, as the last points are added by hand.
        self.add_hole(Point(76.75, -13.35))
        self.add_hole(Point(52.05, -20.02))



class BlissContour(HeadstockContourBase):

    """My first design based on the Music man idea.
    """

    DEFAULT_PAR_DICT = {'width_at_nut': 43.00,
                        'max_width': 75.00,
                        'stub': 10.00,
                        'main_slope': 15.00,
                        'main_radius': 24.00,
                        'corner_radius': 3.5
                        }

    def construct(self):
        """Overloaded method.
        """
        r1 = 12.
        span1 = 60.
        span3 = 160.
        offset3 = -0.26

        top = 0.5 * self.max_width
        bot = -top

        p1 = self.anchor.vmove(0.5 * self.width_at_nut)
        line1 = Line(p1, p1.hmove(self.stub))
        arc1 = line1.connecting_circular_arc(r1, span1)
        # Calculate the length of the line that brings the very top of the
        # following rounding circle to be at the y of the top parameter.
        alpha = np.radians(arc1.end_slope())
        dh = self.corner_radius * (1. - np.cos(alpha))
        l = (top - arc1.end_point().y - dh) / np.sin(alpha)
        line2 = arc1.connecting_line(l)
        span = line2.slope() + self.main_slope
        arc2 = line2.connecting_circular_arc(-self.corner_radius, -span)
        # At this point the y coordinate of the top of the small rounding arc
        # should be exactly top.
        assert arc2.center.vmove(-arc2.radius).y == top
        # The end point of the next line must be such that the center of the
        # big circle goes where expected.
        hc = offset3 * self.width_at_nut
        dh = self.main_radius * np.cos(np.radians(self.main_slope))
        l = (arc2.end_point().y - hc - dh) / np.sin(np.radians(self.main_slope))
        line3 = arc2.connecting_line(-l)
        arc3 = line3.connecting_circular_arc(-self.main_radius, -span3)
        print(arc3.center.y, offset3 * self.width_at_nut)

        arc4 = arc3.connecting_circular_arc(-self.corner_radius, -80.)
        arc5 = arc4.connecting_circular_arc(-17., 90.)
        print(arc5.end_slope() - 180.)

        l = (arc5.end_point().y - bot) / np.sin(np.radians(self.main_slope))
        line4 = arc5.connecting_line(l)
        print(line4.end_point().y, bot)

        arc6 = line4.connecting_circular_arc(-self.corner_radius, -80.)
        #arc7 = arc6.connecting_circular_arc(25., arc6.end_slope())

        c = arc6.center
        dx = c.x - self.stub
        r = dx / np.sin(np.radians(180. - arc6.start_phi)) - self.corner_radius
        slope = arc6.end_phi
        #print(c, slope, dx, r)
        print(arc6.start_phi, arc6.end_phi)

        p1 = self.anchor.vmove(-0.5 * self.width_at_nut)
        line5 = Line(p1, p1.hmove(self.stub))
        arc8 = line5.connecting_circular_arc(-r, arc6.end_phi - 90)

        return locals()
