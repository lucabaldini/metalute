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

"""Pick-up facilities.
"""

from dataclasses import dataclass

import numpy as np

from metalute.units import inches_to_mm
from metalute.blueprint import blueprint
from metalute.matplotlib_ import plt
from metalute.geometry import Point, Line, Circle, Hole, Rectangle, RoundedRectangle, ParametricPolyPathBase, CircularArc



@dataclass
class PickupBase:

    """Base class for a pickup.
    """

    inner_length : float
    inner_width : float
    outer_length : float
    outer_width : float
    string_spacing : float
    screw_spacing : float
    num_strings : int = 6
    magnet_diameter : float = 2.25
    screw_hole_diameter : float = 1.5

    def draw_magnets(self, offset):
        """Draw the magnets.

        This is relevant for both single-coils and humbuckers.
        """
        for i in range(self.num_strings):
            Circle((0., self.string_spacing * (i - 2.5)), self.magnet_diameter).draw(offset)

    def draw_screw_holes(self, offset):
        """Draw the holes for the mounting screws.
        """
        w = 0.5 * self.screw_spacing
        Circle((0., w), self.screw_hole_diameter).draw(offset)
        Circle((0., -w), self.screw_hole_diameter).draw(offset)

    def draw(self, offset):
        """Not implemented.
        """
        raise NotImplementedError



@dataclass
class SingleCoilBase(PickupBase):

    """Base class for a single-coil pickup.
    """

    @staticmethod
    def _draw_contour(length, width, offset):
        """
        """
        r = 0.5 * length
        w = 0.5 * width - r
        l = length - width
        CircularArc((0., w), r, 0., 180.).draw(offset).\
            connecting_line(-l).draw(offset).\
            connecting_circular_arc(r, 180.).draw(offset).\
            connecting_line(-l).draw(offset)

    def draw(self, offset):
        """Overloaded method.
        """
        self._draw_contour(self.inner_length, self.inner_width, offset)
        self._draw_contour(self.outer_length, self.outer_width, offset)
        self.draw_magnets(offset)
        self.draw_screw_holes(offset)


@dataclass
class HumbuckerBase(PickupBase):

    """Base class for a humbucker.
    """

    wing_length : float = 12.
    corner_radius : float = 3.

    def draw_wings(self, offset):
        """
        """
        w = 0.5 * (self.outer_width - self.inner_width) - self.corner_radius
        l = self.wing_length - 2. * self.corner_radius
        p = Point(0.5 * self.wing_length, 0.5 * self.inner_width)
        Line(p, p.vmove(w)).draw(offset).\
            connecting_circular_arc(self.corner_radius, 90.).draw(offset).\
            connecting_line(l).draw(offset).\
            connecting_circular_arc(self.corner_radius, 90.).draw(offset).\
            connecting_line(w).draw(offset)
        p = Point(0.5 * self.wing_length, -0.5 * self.inner_width)
        Line(p, p.vmove(-w)).draw(offset).\
            connecting_circular_arc(-self.corner_radius, -90.).draw(offset).\
            connecting_line(-l).draw(offset).\
            connecting_circular_arc(-self.corner_radius, -90.).draw(offset).\
            connecting_line(-w).draw(offset)

    def draw(self, offset):
        """Overloaded method.
        """
        l = 0.5 * self.inner_length
        w = self.inner_width
        d = Point(0.5 * l, 0.)
        SingleCoilBase._draw_contour(l, w, offset - d)
        self.draw_magnets(offset - d)
        SingleCoilBase._draw_contour(l, w, offset + d)
        self.draw_magnets(offset + d)
        self.draw_screw_holes(offset)
        RoundedRectangle((0., 0.), self.inner_length, self.inner_width, self.corner_radius).draw(offset)
        self.draw_wings(offset)



@dataclass
class SingleCoilEMG(SingleCoilBase):

    """EMG-S, SA, SV, SAV, SLV

    https://www.emgpickups.com/pub/media/Mageants/s/_/s_pickups_0230-0109rd.pdf
    """

    inner_length : float = 17.78
    inner_width : float = 69.85
    outer_length : float = inner_length
    outer_width : float = 83.3
    string_spacing : float = 10.46
    screw_spacing : float = 76.2

    def draw(self, offset):
        """Overloaded method.

        We overload this because the magnets are hidden by the plastic cover.
        """
        self._draw_contour(self.inner_length, self.inner_width, offset)
        self._draw_contour(self.outer_length, self.outer_width, offset)
        self.draw_screw_holes(offset)



@dataclass
class HumbuckerDiMarzio(HumbuckerBase):

    """
    """

    inner_length : float = inches_to_mm(1.5)
    inner_width : float = inches_to_mm(2.7)
    outer_length : float = inner_length
    outer_width : float = inches_to_mm(3.32)
    string_spacing : float = inches_to_mm(0.383)
    screw_spacing : float = inches_to_mm(3.1)
    wing_length : float = inches_to_mm(0.515)





class PickupSlot(Rectangle):

    def __init__(self, width, height, name=None):
        """Constructor.
        """
        super().__init__(Point(0., 0.), width, height, name)



class SingleCoilSlot(PickupSlot):

    def __init__(self, width=20., height=70., name=None):
        """
        """
        super().__init__(width, height, name)



class HumbuckerSlot(PickupSlot):

    def __init__(self, width=40., height=88., name=None):
        """
        """
        super().__init__(width, height, name)




class SingleCoilRouting(ParametricPolyPathBase):

    """Class for a parametric routing template for a single-coil pickup.

    The dimensions of the various available routings vary, and the default
    parameters for this object are a more or less sensible compilation based
    on both web resources and direct measurements.

    A few pointers:

    * https://www.reddit.com/r/Luthier/comments/db76l6/single_coil_strat_routing_template_dimensions/
    """

    DEFAULT_PAR_DICT = {'w': 20.,
                        'h': 88.,
                        'r': 9.999999999999
                        }

    def construct(self):
        """Overloaded method.
        """
        d1 = self.h - 2. * self.r
        d2 = self.w - 2. * self.r
        c = self.anchor + Point(0.5 * self.w - self.r, 0.5 * self.h - self.r)
        arc1 = CircularArc(c, self.r, 90., -90.)
        hole1 = Hole(arc1.center, 2. * self.r, 1.)
        line1 = arc1.connecting_line(d1)
        arc2 = line1.connecting_circular_arc(-self.r, -90.)
        hole2 = Hole(arc2.center, 2. * self.r, 1.)
        line2 = arc2.connecting_line(-d2)
        arc3 = line2.connecting_circular_arc(-self.r, -90.)
        hole3 = Hole(arc3.center, 2. * self.r, 1.)
        line3 = arc3.connecting_line(-d1)
        arc4 = line3.connecting_circular_arc(-self.r, -90.)
        hole4 = Hole(arc4.center, 2. * self.r, 1.)
        line4 = arc4.connecting_line(-d2)
        return locals()




class HumbuckerRouting(ParametricPolyPathBase):

    """Class for a parametric routing template for a humbucking pickup.

    The dimensions of the various available routings vary, and the default
    parameters for this object are a more or less sensible compilation based
    on both web resources and direct measurements.

    A few pointers:

    * https://shoppartsland.com/pickup-routing-template-humbucker/
    * https://www.tdpri.com/threads/humbucker-routing-help.423806/
    """

    DEFAULT_PAR_DICT = {'w1': 20.,
                        'w2': 40.,
                        'h1': 72.,
                        'h2': 88.,
                        'r': 3.
                        }

    def construct(self):
        """Overloaded method.
        """
        d1 = 0.5 * (self.w2 - self.w1) - self.r
        d2 = 0.5 * (self.h2 - self.h1) - self.r
        d3 = self.w1 - 2. * self.r
        c = self.anchor + Point(0.5 * self.w2 - self.r, 0.5 * self.h1 - self.r)
        arc1 = CircularArc(c, self.r, 90., -90.)
        hole1 = Hole(arc1.center, 2. * self.r, 1.)
        line1 = arc1.connecting_line(self.h1 - 2. * self.r)
        arc2 = line1.connecting_circular_arc(-self.r, -90.)
        hole2 = Hole(arc2.center, 2. * self.r, 1.)
        line2 = arc2.connecting_line(-d1)
        p1 = line2.end_point()
        line3 = Line(p1, p1.vmove(-d2))
        arc3 = line3.connecting_circular_arc(-self.r, -90.)
        hole3 = Hole(arc3.center, 2. * self.r, 1.)
        line4 = arc3.connecting_line(-d3)
        arc4 = line4.connecting_circular_arc(-self.r, -90.)
        hole4 = Hole(arc4.center, 2. * self.r, 1.)
        line5 = arc4.connecting_line(-d2)
        p2 = line5.end_point()
        line6 = Line(p2, p2.hmove(-d1))
        arc5 = line6.connecting_circular_arc(-self.r, -90.)
        hole5 = Hole(arc5.center, 2. * self.r, 1.)
        line7 = arc5.connecting_line(-self.h1 + 2. * self.r)
        arc6 = line7.connecting_circular_arc(-self.r, -90.)
        hole6 = Hole(arc6.center, 2. * self.r, 1.)
        line8 = arc6.connecting_line(-d1)
        p3 = line8.end_point()
        line9 = Line(p3, p3.vmove(d2))
        arc7 = line9.connecting_circular_arc(-self.r, -90.)
        hole7 = Hole(arc7.center, 2. * self.r, 1.)
        line10 = arc7.connecting_line(-d3)
        arc8 = line10.connecting_circular_arc(-self.r, -90.)
        hole8 = Hole(arc8.center, 2. * self.r, 1.)
        line11 = arc8.connecting_line(-d2)
        p4 = line11.end_point()
        line12 = Line(p4, p4.hmove(d1))
        return locals()



if __name__ == '__main__':
    blueprint('Single coil', 'A4')
    p = SingleCoilEMG()
    print(p)
    p.draw(Point(-50., 0.))

    p = HumbuckerDiMarzio()
    p.draw(Point(0., 0.))

    plt.show()
