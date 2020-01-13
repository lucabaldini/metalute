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

from metalute.geometry import Point, Line, CircleArc, SpiralArc


class MusicManAxis:

    """
    """

    DEFAULT_PARAMS = {'d1': 240.00,
                      'm1': 151.07,
                      'q1': 89.54,
                      'scale1': 120.97,
                      'gamma1': 5.4759
                      }

    def __init__(self):
        """Constructor.
        """
        pass

    @staticmethod
    def big_radius(phi, m, q, scale, gamma):
        """
        """
        _phi = phi - 2. * (phi - 180.) * (phi > 180.)
        return q + m * (1. - np.exp(-(_phi / scale)**gamma))

    def draw(self, offset):
        """
        """
        d1 = 240.00
        m1 = 151.07
        q1 = 89.54
        scale1 = 120.97
        gamma1 = 5.4759
        phi1 = 100.
        phi2 = 240.
        d2 = 25.
        r3 = 91.50
        phi3 = 70.

        anchor = Point(0., 0., 'anchor')
        c1 = anchor.move(d1, 0., 'c1')
        radius = lambda phi: MusicManAxis.big_radius(phi, m1, q1, scale1, gamma1)
        arc1 = SpiralArc(c1, radius, phi1, phi2)
        arc1.draw(offset)
        p1 = arc1.start_point('p1')
        p1.draw(offset)
        phi = arc1.slope_at_start_point()
        p2 = p1.move(d2, phi, 'p2')
        p2.draw(offset)
        line = Line(p1, p2)
        line.draw(offset)
        c3 = p2.move(r3, phi + 90.)
        c3.draw(offset)
        arc3 = CircleArc(c3, r3, phi - 90., phi - 90. + phi3)
        arc3.draw(offset)
