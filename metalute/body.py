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
        phi1 = 100.00
        phi2 = 240.00
        d2 = 25.00
        r3 = 91.50
        phi3 = 55.00
        r4 = 140.00
        phi4 = 20.00
        r5 = 33.54
        phi5 = 148.00
        r6 = 30.00
        phi6 = 99.00
        r7 = 22.54
        phi7 = 110.00
        r8 = 102.10
        phi8 = 27.00
        r9 = 34.53
        phi9 = 165.00
        r10 = 16.61
        phi10 = 150.
        r11 = 65.83
        phi11 = 37.00
        r12 = 72.25
        phi12 = 60.00
        r13 = 180.00
        phi13 = 25. # removeme

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
        line1 = Line(p1, p2)
        line1.draw(offset)
        c3 = p2.move(r3, phi + 90., 'c3')
        c3.draw(offset)
        arc3 = CircleArc(c3, r3, phi - 90., phi - 90. + phi3)
        arc3.draw(offset)
        p3 = arc3.end_point('p3')
        p3.draw(offset)
        c4 = p3.move(r4, arc3.phi2, 'c4')
        arc4 = CircleArc(c4, r4, arc3.phi2 - phi4 + 180., arc3.phi2 + 180.)
        arc4.draw(offset)
        p4 = arc4.start_point('p4')
        p4.draw(offset)
        c5 = p4.move(r5, arc4.phi1 + 180., 'c5')
        arc5 = CircleArc(c5, r5, arc4.phi1 - phi5, arc4.phi1)
        arc5.draw(offset)
        p5 = arc5.start_point('p5')
        p5.draw(offset)
        c6 = p5.move(r6, arc5.phi1, 'c6')
        arc6 = CircleArc(c6, r6, arc5.phi1 + 180., arc5.phi1 + phi6 + 180.)
        arc6.draw(offset)
        p7 = arc6.end_point('p7')
        p7.draw(offset)
        c7 = p7.move(r7, arc6.phi2, 'c7')
        arc7 = CircleArc(c7, r7, arc6.phi2 + 180. - phi7, arc6.phi2 + 180.)
        arc7.draw(offset)
        p8 = arc7.start_point('p8')
        p8.draw(offset)
        c8 = p8.move(r8, arc7.phi1 + 180., 'c8')
        arc8 = CircleArc(c8, r8, arc7.phi1 - phi8, arc7.phi1)
        arc8.draw(offset)
        p9 = arc8.start_point('p9')
        p9.draw(offset)
        c9 = p9.move(r9, arc8.phi1, 'c9')
        arc9 = CircleArc(c9, r9, arc8.phi1 + 180, arc8.phi1 + 180. + phi9)
        arc9.draw(offset)
        p10 = arc9.end_point('p10')
        p10.draw(offset)
        c10 = p10.move(r10, arc9.phi2, 'c10')
        arc10 = CircleArc(c10, r10, arc9.phi2 - 180. - phi10, arc9.phi2 - 180.)
        arc10.draw(offset)
        p11 = arc10.start_point('p11')
        p11.draw(offset)
        c11 = p11.move(r11, arc10.phi1 + 180., 'c11')
        arc11 = CircleArc(c11, r11, arc10.phi1 - phi11, arc10.phi1)
        arc11.draw(offset)
        p12 = arc11.start_point('p12')
        p12.draw(offset)
        c12 = p12.move(r12, arc11.phi1, 'c12')
        arc12 = CircleArc(c12, r12, arc11.phi1 + 180., arc11.phi1 + 180 + phi12)
        arc12.draw(offset)
        p13 = arc12.end_point('p13')
        p13.draw(offset)
        c13 = p13.move(r13, arc12.phi2, 'c13')
        arc13 = CircleArc(c13, r13, arc12.phi2 + 180. - phi13, arc12.phi2 + 180.)
        arc13.draw(offset)
