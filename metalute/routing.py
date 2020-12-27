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

from metalute.matplotlib_ import plt
from metalute.blueprint import blueprint
from metalute.geometry import Point, Rectangle, Hole
from metalute.pickup import SingleCoilRouting, HumbuckerRouting


class RoutingTemplateBase:

    """
    """

    def __init__(self, width, height):
        """
        """
        self.width = width
        self.height = height
        self.center = Point(0., 0.)

    def draw(self, offset):
        """
        """
        Rectangle(self.center, self.width, self.height).draw(offset)
        plt.hlines(0, -0.5 * self.width, 0.5 * self.width)
        plt.vlines(0, -0.5 * self.height, 0.5 * self.height)
        Hole(self.center.vmove(0.5 * self.height), 1.5).draw(offset)
        Hole(self.center.vmove(-0.5 * self.height), 1.5).draw(offset)
        Hole(self.center.hmove(0.5 * self.width), 1.5).draw(offset)
        Hole(self.center.hmove(-0.5 * self.width), 1.5).draw(offset)
        Hole(self.center.vmove(0.5 * self.height - 10.), 3.).draw(offset)
        Hole(self.center.vmove(-0.5 * self.height + 10.), 3.).draw(offset)
        Hole(self.center.hmove(0.5 * self.width - 10.), 3.).draw(offset)
        Hole(self.center.hmove(-0.5 * self.width + 10.), 3.).draw(offset)


    def draw_text(self, offset, text):
        """
        """
        p = Point(-0.45 * self.width, -0.45 * self.height) + offset
        plt.text(p.x, p.y, text)



class PickupRoutingTemplate(RoutingTemplateBase):

    """
    """

    def __init__(self, routing_class, width=125., height=200., **params):
        """
        """
        super().__init__(width, height)
        self.routing = routing_class(**params)

    def draw(self, offset):
        """
        """
        super().draw(offset)
        self.routing.draw(offset)
        #self.draw_text(offset, self.routing.par_dict)



class SingleCoilRoutingTemplate(PickupRoutingTemplate):

    """
    """

    def __init__(self, width=125., height=200., **params):
        """
        """
        super().__init__(SingleCoilRouting, width, height, **params)



class HumbuckerRoutingTemplate(PickupRoutingTemplate):

    """
    """

    def __init__(self, width=125., height=200., **params):
        """
        """
        super().__init__(HumbuckerRouting, width, height, **params)




if __name__ == '__main__':
    blueprint('Single-coil Routing Template', 'A4', 'Luca Baldini', orientation='Portrait')
    t = SingleCoilRoutingTemplate()
    t.draw(Point(0., 0.))
    plt.savefig('single_coil_routing_template.pdf')


    blueprint('Humbucker Routing Template', 'A4', 'Luca Baldini', orientation='Portrait')
    t = HumbuckerRoutingTemplate()
    t.draw(Point(0., 0.))
    plt.savefig('humbucker_routing_template.pdf')

    plt.show()
