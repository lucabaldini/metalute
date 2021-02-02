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



@dataclass
class Workbench(Drawable):

    """
    """
    width : float = 1000.
    height : float = 500.
    base_width : float = 850.
    base_stud_thickness : float = 25.
    corner_radius : float = 10.
    hole_pitch : float = 100.
    hole_diameter : float = 8.
    channel_width : float = 8.

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        center = Point(0., 0.)
        rectangle(center, self.width, self.height, self.corner_radius, offset)
        d = 0.5 * (self.height - self.base_stud_thickness)
        rectangle(center.vmove(-d), self.base_width, self.base_stud_thickness, 0., offset, ls='dashed')
        rectangle(center.vmove(d), self.base_width, self.base_stud_thickness, 0., offset, ls='dashed')
        d = 0.5 * (self.base_width + self.base_stud_thickness)
        rectangle(center.hmove(-d), self.base_stud_thickness, self.height, 0., offset, ls='dashed')
        rectangle(center.hmove(d), self.base_stud_thickness, self.height, 0., offset, ls='dashed')
        d /= 3.
        h = self.height - 2. * self.base_stud_thickness
        rectangle(center.hmove(-d), self.base_stud_thickness, h, 0., offset, ls='dashed')
        rectangle(center.hmove(d), self.base_stud_thickness, h, 0., offset, ls='dashed')
        # Hole grid and channels.
        h = 4. * self.hole_pitch + self.hole_diameter
        for i in range(-4, 5):
            for j in range(-2, 3):
                if i in  [-3, 0, 3]:
                    p = Point(i * self.hole_pitch, 0.)
                    rectangle(p, self.channel_width, h, 0.4999 * self.channel_width, offset)
                else:
                    c = Point(i * self.hole_pitch, j * self.hole_pitch)
                    hole(c, self.hole_diameter, offset=offset)



if __name__ == '__main__':
    blueprint('Jigsaw jig', 'A1')
    JigsawJig().draw()

    blueprint('Workbench', 'A0', orientation='Landscape')
    Workbench().draw()
    plt.show()
