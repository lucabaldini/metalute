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


from dataclasses import dataclass

import numpy as np

from metalute.blueprint import blueprint
from metalute.geometry2 import Drawable, Point, line, rectangle, circle, hole
from metalute.matplotlib_ import plt



@dataclass
class JigsawJig(Drawable):

    """Cut straight lines with a jigsaw?
    """

    length : float = 500.
    head_radius : float = 15.
    border_width : float = 20
    channel_width : float = 80.
    pin_hole_diameter : float = 6.
    hole_diameter = 30.

    def __post_init__(self):
        """
        """
        self.width = self.channel_width + 2. * self.border_width

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        # Draw the outer contour.
        w = 0.5 * self.width
        p = Point(0.5 * self.length + 0.5 * w, w) + offset
        l = 0.5 * self.width * np.sqrt(2.) - self.head_radius
        _arc = line(p, p.hmove(-self.length)).draw_connecting_line(l, 225.).\
            draw_connecting_arc(self.head_radius, 90.)
        _arc.draw_connecting_line(l).draw_connecting_line(self.length, 0.).\
            draw_connecting_line(self.width, 90.)
        # The pin hole.
        hole(_arc.center, self.pin_hole_diameter)
        # The two borders.
        c = Point(0.5 * w, 0.5 * (self.channel_width + self.border_width)) + offset
        rectangle(c, self.length, self.border_width)
        c = c.vmove(-self.channel_width - self.border_width)
        rectangle(c, self.length, self.border_width)
        # The two big holes.
        c = Point(p.x - self.hole_diameter, 0.)
        hole(c, self.hole_diameter)
        hole(c.hmove(-self.length + 2. * self.hole_diameter), self.hole_diameter)
        line(c.hmove(-0.5 * self.hole_diameter), c.hmove(-self.length + 2.5 * self.hole_diameter))



if __name__ == '__main__':
    blueprint('Jigsaw jig', 'A1')
    JigsawJig().draw()
    plt.show()
