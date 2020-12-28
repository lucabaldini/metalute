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

from dataclasses import dataclass, asdict

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
        """Draw the contour of the pickup body.

        This is factored out as a staticmethod because it will be reused in
        drawing humbukers.
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
        self._draw_contour(self.inner_length, self.outer_width, offset)
        if self.outer_length != self.inner_length:
            w = 0.5 * self.inner_width - 0.25 * self.inner_length
            d = 6.
            p1 = Point(-0.5 * self.inner_length, w)
            p2 = Point(p1.x - self.outer_length + self.inner_length, d)
            p3 = p2.vmove(-2. * d)
            p4 = Point(-0.5 * self.inner_length, -w)
            Line(p1, p2).draw(offset)
            Line(p2, p3).draw(offset)
            Line(p3, p4).draw(offset)
        self.draw_magnets(offset)
        self.draw_screw_holes(offset)



@dataclass
class HumbuckerBase(PickupBase):

    """Base class for a humbucker.
    """

    wing_length : float = 12.
    corner_radius : float = 3.

    def draw_wings(self, offset):
        """Draw the hanging metal wings with the screw holes.
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

    """Geometry for EMG-S, SA, SV, SAV, SLV

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
class SingleCoilDiMarzio(SingleCoilBase):

    """Geometry for Di Marzio Strat single coils.

    https://d2emr0qhzqfj88.cloudfront.net/s3fs-public/diagrams/scdimensions_0.pdf
    """

    inner_length : float = inches_to_mm(0.69)
    inner_width : float = inches_to_mm(2.74)
    outer_length : float = inches_to_mm(0.90)
    outer_width : float = inches_to_mm(3.28)
    string_spacing : float = inches_to_mm(0.406)
    screw_spacing : float = inches_to_mm(3.02)



@dataclass
class HumbuckerEMG(HumbuckerBase):

    """Geometry for most EMG humbuckers.

    https://www.emgpickups.com/pub/media/Mageants/h/x/hx_0230-0110re.pdf
    """

    inner_length : float = 38.1
    inner_width : float = 69.8
    outer_length : float = inner_length
    outer_width : float = 83.0 # TBC
    string_spacing : float = inches_to_mm(0.383) # TBC
    screw_spacing : float = 78.5
    wing_length : float = inches_to_mm(0.500) # TBC

    def draw(self, offset):
        """Overloaded method.
        """
        self.draw_screw_holes(offset)
        RoundedRectangle((0., 0.), self.inner_length, self.inner_width, self.corner_radius).draw(offset)
        self.draw_wings(offset)




@dataclass
class HumbuckerDiMarzio(HumbuckerBase):

    """Geometry for most Di Marzio humbuckers.

    https://d2emr0qhzqfj88.cloudfront.net/s3fs-public/diagrams/DMHBdim_0.pdf
    """

    inner_length : float = inches_to_mm(1.5)
    inner_width : float = inches_to_mm(2.7)
    outer_length : float = inner_length
    outer_width : float = inches_to_mm(3.32)
    string_spacing : float = inches_to_mm(0.383)
    screw_spacing : float = inches_to_mm(3.1)
    wing_length : float = inches_to_mm(0.515)



@dataclass
class HumbuckerDiMarzioF(HumbuckerDiMarzio):

    """Geometry for most Di Marzio F-spaced humbuckers.

    https://d2emr0qhzqfj88.cloudfront.net/s3fs-public/diagrams/DMHBdim_0.pdf
    """

    string_spacing : float = inches_to_mm(0.402)



@dataclass
class HumbuckerSeymourDuncan(HumbuckerBase):

    """Geometry for most Seymour Duncan humbuckers.

    https://www.seymourduncan.com/wp-content/uploads/2019/08/HB-6-String-Uncovered-Short-Magnet-Long-Leg-Bottom-Plate.gif
    """

    inner_length : float = inches_to_mm(1.438)
    inner_width : float = inches_to_mm(2.695)
    outer_length : float = inner_length
    outer_width : float = inches_to_mm(3.315)
    string_spacing : float = inches_to_mm(0.385)
    screw_spacing : float = inches_to_mm(3.063)
    wing_length : float = inches_to_mm(0.500)



@dataclass
class RoutingBase:

    """
    """

    def draw_parameters(self, offset, line_spacing=6.):
        """
        """
        y = 0.
        params = asdict(self)
        keys = list(params.keys())
        keys.reverse()
        for key in keys:
            value = params[key]
            key = key.replace('_', ' ')
            plt.text(offset.x, offset.y - y, f'{key} = {value} mm')
            y -= line_spacing



@dataclass
class SingleCoilRouting(RoutingBase):

    """Class for a parametric routing template for a single-coil pickup.

    The dimensions of the various available routings vary, and the default
    parameters for this object are a more or less sensible compilation based
    on both web resources and direct measurements.
    """

    inner_length : float = 21.
    outer_length : float = 27.
    width : float = 87.
    flat_width : float = 18.

    def draw(self, offset):
        """
        """
        radius = 0.5 * self.inner_length
        a = self.outer_length - self.inner_length
        b = 0.5 * (self.width - self.flat_width) - radius
        theta = (-b + np.sqrt(b**2. + 2 * a * radius)) / radius
        l = np.sqrt((a + 0.5 * radius * theta**2.)**2. + (b + radius * theta)**2.)
        p = Point(0., 0.5 * self.width - radius)
        line = CircularArc(p, radius, 0., 180. - np.degrees(theta)).draw(offset).\
            connecting_line(l).draw(offset)
        p = line.end_point()
        Line(p, p.vmove(-self.flat_width)).draw(offset)
        p = Point(0., - 0.5 * self.width + radius)
        line = CircularArc(p, radius, 0., -180. + np.degrees(theta)).draw(offset).\
            connecting_line(l).draw(offset)
        p = p.hmove(0.5 * self.inner_length)
        Line(p, p.vmove(self.width - 2. * radius)).draw(offset)



@dataclass
class HumbuckerRouting(RoutingBase):

    """Class for a parametric routing template for a humbucking pickup.

    The dimensions of the various available routings vary, and the default
    parameters for this object are a more or less sensible compilation based
    on both web resources and direct measurements.
    """

    length : float = 41.
    inner_width : float = 72.
    outer_width : float = 87.
    wing_length : float = 16.
    corner_radius : float = 3.

    def _draw_cap(self, start_point, start_phi, d1, d2, offset):
        """convenience function to draw a half rectangle with rounded borders.
        """
        line = Line(start_point, start_point.move(d1, start_phi)).draw(offset).\
            connecting_circular_arc(self.corner_radius, 90.).draw(offset).\
            connecting_line(d2).draw(offset).\
            connecting_circular_arc(self.corner_radius, 90.).draw(offset).\
            connecting_line(d1).draw(offset)
        return line

    def draw(self, offset, drilling_holes=False):
        """Draw the routing.
        """
        l1 = 0.5 * (self.length - self.wing_length) - self.corner_radius
        l2 = self.wing_length - 2. * self.corner_radius
        w1 = self.inner_width - 2. * self.corner_radius
        w2 = 0.5 * (self.outer_width - self.inner_width) - self.corner_radius
        p = Point(0.5 * self.wing_length, 0.5 * self.inner_width)
        line = self._draw_cap(p, 90., w2, l2, offset)
        p = line.end_point()
        line = self._draw_cap(p, 180., l1, w1, offset)
        p = line.end_point()
        line = self._draw_cap(p, -90., w2, l2, offset)
        p = line.end_point()
        line = self._draw_cap(p, 0., l1, w1, offset)
        if drilling_holes:
            l = self.length - 2. * self.corner_radius
            w = self.inner_width - 2. * self.corner_radius
            for p in Rectangle((0., 0.), l, w).points:
                Hole(p, 2 * self.corner_radius, 1.).draw(offset)
            l = self.wing_length - 2. * self.corner_radius
            w = self.outer_width - 2. * self.corner_radius
            for p in Rectangle((0., 0.), l, w).points:
                Hole(p, 2 * self.corner_radius, 1.).draw(offset)



if __name__ == '__main__':
    blueprint('Single coil', 'A4')
    offset = Point(0., 0.)
    SingleCoilEMG().draw(offset)
    SingleCoilRouting().draw(offset)
    offset = Point(50., 0.)
    SingleCoilDiMarzio().draw(offset)
    SingleCoilRouting().draw(offset)

    blueprint('Humbuckers', 'A4')
    offset = Point(-75., 0.)
    HumbuckerDiMarzio().draw(offset)
    HumbuckerRouting().draw(offset)
    offset = Point(-0., 0.)
    HumbuckerEMG().draw(offset)
    HumbuckerRouting().draw(offset)
    offset = Point(75., 0.)
    HumbuckerSeymourDuncan().draw(offset)
    HumbuckerRouting().draw(offset)

    plt.show()
