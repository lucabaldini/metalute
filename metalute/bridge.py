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

"""Bridge facilities.
"""

import numpy as np

from metalute.geometry import Point, Line, Rectangle, ParametricPolyPathBase, CircularArc, Hole


class HardtailBridgeBase(ParametricPolyPathBase):

    DEFAULT_PAR_DICT = {'w': 41.,
                        'd': 16.,
                        'h': 65.,
                        'r': 5.,
                        'hs': 42.,
                        'hd': 4.,
                        'hp': 6.
                        }

    def construct(self):
        """Overloaded method.
        """
        p1 = self.anchor + Point(-self.w + self.d, 0.5 * self.h)
        line1 = Line(p1, p1.hmove(self.w - self.r))
        arc1 = line1.connecting_circular_arc(-self.r, -90.)
        line2 = arc1.connecting_line(-self.h + 2. * self.r)
        arc2 = line2.connecting_circular_arc(-self.r, -90.)
        line3 = arc2.connecting_line(-self.w + self.r)
        line4 = Line(line3.end_point(), p1)
        h1 = Hole(Point(self.d - self.hp, 0.5 * self.hs), self.hd)
        h2 = Hole(Point(self.d - self.hp, -0.5 * self.hs), self.hd)
        h3 = Hole(Point(-self.w + self.d + self.hp, 0.5 * self.hs), self.hd)
        h4 = Hole(Point(-self.w + self.d + self.hp, -0.5 * self.hs), self.hd)
        return locals()
