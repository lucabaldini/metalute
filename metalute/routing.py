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

"""Miscellanea routing templates.
"""

import numpy as np

from metalute import GITHUB_URL
from metalute.matplotlib_ import plt
from metalute.blueprint import blueprint
from metalute.geometry import Point, Rectangle, Hole
from metalute.pickup import SingleCoilRouting, HumbuckerRouting



class RoutingTemplateBase:

    """Base class for a routing template.

    This is essentially a rectangle with the center lines and some reference
    holes.

    Note this class should not be instantiated.
    """

    LENGTH = None
    WIDTH = None
    CENTER = Point(0., 0.)
    BORDER = 10.

    def draw(self, offset):
        """Fundamental draw method.
        """
        # The big rectangle.
        l = 0.5 * self.LENGTH
        w = 0.5 * self.WIDTH
        Rectangle(self.CENTER, self.LENGTH, self.WIDTH).draw(offset)
        # The two center lines.
        plt.hlines(0, -l, l)
        plt.vlines(0, -w, w)
        # Small centering holes.
        r = 1.5
        Hole(self.CENTER.vmove(w), r).draw(offset)
        Hole(self.CENTER.vmove(-w), r).draw(offset)
        Hole(self.CENTER.hmove(l), r).draw(offset)
        Hole(self.CENTER.hmove(-l), r).draw(offset)
        # Bigger centering holes.
        r = 3.
        Hole(self.CENTER.vmove(w - self.BORDER), r).draw(offset)
        Hole(self.CENTER.vmove(-w + self.BORDER), r).draw(offset)
        Hole(self.CENTER.hmove(l - self.BORDER), r).draw(offset)
        Hole(self.CENTER.hmove(-l + self.BORDER), r).draw(offset)
        # And, finally, the branding :-)
        x = -l + self.BORDER + offset.x
        y = w - 2. * self.BORDER + offset.y
        plt.text(x, y, GITHUB_URL)



class PickupRoutingTemplateBase(RoutingTemplateBase):

    """Base class for a pickup routing template.
    """

    LENGTH = 125.
    WIDTH = 200.

    def __init__(self, routing_class, **params):
        """Constructor.
        """
        self.routing = routing_class(**params)

    def draw(self, offset, **kwargs):
        """Overloaded method.
        """
        super().draw(offset)
        self.routing.draw(offset, **kwargs)
        p = Point(-0.5 * self.LENGTH + self.BORDER, -0.5 * self.WIDTH + self.BORDER)
        self.routing.draw_parameters(offset + p)



class SingleCoilRoutingTemplate(PickupRoutingTemplateBase):

    """Single-coil pickup routing template.
    """

    def __init__(self, **params):
        """Constructor.
        """
        super().__init__(SingleCoilRouting, **params)



class HumbuckerRoutingTemplate(PickupRoutingTemplateBase):

    """Humbucker pickup routing template.
    """

    def __init__(self, **params):
        """Constructor.
        """
        super().__init__(HumbuckerRouting, **params)



class NeckPocketRoutingTemplate(RoutingTemplateBase):

    """Neck routing template.
    """

    LENGTH = 280.
    WIDTH = 140.




if __name__ == '__main__':
    offset = Point(0., 0.)

    blueprint('Single-coil Routing Template', 'A4', 'Luca Baldini', orientation='Portrait')
    SingleCoilRoutingTemplate().draw(offset)
    plt.savefig('single_coil_routing_template.pdf')

    blueprint('Humbucker Routing Template', 'A4', 'Luca Baldini', orientation='Portrait')
    HumbuckerRoutingTemplate().draw(offset, drilling_holes=True)
    plt.savefig('humbucker_routing_template.pdf')

    blueprint('Neck Pocket Routing Template', 'A3', 'Luca Baldini', orientation='Landscape')
    NeckPocketRoutingTemplate().draw(offset)

    plt.show()
