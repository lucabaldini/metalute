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


from dataclasses import dataclass

import numpy as np

from metalute.blueprint import blueprint
from metalute.geometry2 import Drawable, Point, line, vline, rectangle, circle, hole
from metalute.matplotlib_ import plt



class DrillPress(Drawable):

    """
    """

    width : float = 180.
    height : float = 120.
    mandrel_diameter : float = 40.
    head_radius : float = 40.

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        p = Point(0., 0.) + offset
        hole(p, self.mandrel_diameter)
        p = p.hmove(-0.75 * self.width)
        slope = -np.degrees(np.arctan2(0.5 * (self.height - self.mandrel_diameter), self.width))
        l = 0.85 * self.width
        vline(p.vmove(-0.4 * self.height), self.height).\
            draw_connecting_line(l, slope).\
            draw_connecting_arc(self.head_radius, -180. + 2. * abs(slope)).\
            draw_connecting_line(l)




if __name__ == '__main__':
    blueprint('Jigsaw jig', 'A4')
    DrillPress().draw(Point(50., 0.))
    plt.show()
