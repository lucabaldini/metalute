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

"""Guitar body.
"""

import numpy as np

from metalute.geometry import SpiralArc, ParametricPolyPathBase


class MusicManAxis(ParametricPolyPathBase):

    """Layout of the Music Man Axis guitar body.
    """

    DEFAULT_PAR_DICT  =  dict(d1 = 240.00,
                              m1 = 151.07,
                              q1 = 89.54,
                              scale1 = 120.97,
                              gamma1 = 5.4759,
                              start_phi1 = 240.,
                              span1 = -140.,
                              d2 = 25.00,
                              r3 = 91.50,
                              span3 = 55.00,
                              r4 = 140.00,
                              span4 = 20.00,
                              r5 = 33.54,
                              span5 = 148.00,
                              r6 = 30.00,
                              span6 = 99.00,
                              r7 = 22.54,
                              span7 = 110.00,
                              r8 = 102.10,
                              span8 = 27.00,
                              r9 = 34.53,
                              span9 = 165.00,
                              r10 = 16.61,
                              span10 = 150.,
                              r11 = 65.83,
                              span11 = 42.00,
                              r12 = 52.25,
                              span12 = 68.00,
                              r13 = 180.00,
                              span13  =  25.
                              )

    @staticmethod
    def big_radius(phi, m, q, scale, gamma):
        """Custom definition of the angular dependence of the radius.
        """
        phi = phi - 2. * (phi - 180.) * (phi > 180.)
        return q + m * (1. - np.exp(-(phi / scale)**gamma))

    def construct(self):
        """Overloaded method.
        """
        c = self.anchor.hmove(self.d1)
        params = self.m1, self.q1, self.scale1, self.gamma1
        radius = lambda phi: MusicManAxis.big_radius(phi, *params)
        arc1 = SpiralArc(c, radius, self.start_phi1, self.span1)
        line1 = arc1.connecting_line(self.d2)
        arc3 = line1.connecting_circular_arc(self.r3, self.span3)
        arc4 = arc3.connecting_circular_arc(-self.r4, self.span4)
        arc5 = arc4.connecting_circular_arc(self.r5, self.span5)
        arc6 = arc5.connecting_circular_arc(-self.r6, self.span6)
        arc7 = arc6.connecting_circular_arc(-self.r7, self.span7)
        arc8 = arc7.connecting_circular_arc(self.r8, self.span8)
        arc9 = arc8.connecting_circular_arc(-self.r9, self.span9)
        arc10 = arc9.connecting_circular_arc(-self.r10, self.span10)
        arc11 = arc10.connecting_circular_arc(self.r11, self.span11)
        arc12 = arc11.connecting_circular_arc(-self.r12, self.span12)
        arc13 = arc12.connecting_circular_arc(-self.r13, self.span13)
        return locals()
