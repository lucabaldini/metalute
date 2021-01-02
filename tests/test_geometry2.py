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

"""Test suite for the units module.
"""

import unittest
import sys

import numpy as np

from metalute.blueprint import blueprint
from metalute.geometry2 import *
from metalute.matplotlib_ import plt
if sys.flags.interactive:
    plt.ion()


class TestGeometry(unittest.TestCase):

    """Unit tests for the geometry module.
    """

    def test_point(self):
        """
        """
        p1 = Point(1., 1.)
        p2 = Point(2., 2.)
        print(p1)
        print(p2)
        # Test point arithmetic.
        self.assertEqual(p1 + p2, Point(3., 3.))
        self.assertEqual(p1 - p2, Point(-1., -1.))
        self.assertEqual(2 * p1, Point(2., 2.))
        self.assertEqual(p1 / 2, Point(0.5, 0.5))

    def test_arc(self):
        """
        """
        blueprint('Test arcs', 'A4')
        center = Point()
        radius = 50.
        span = 15.
        length = 20.
        offset = Point(20., 20.)
        for start_angle in np.linspace(0., 360., 9):
            arc(center, radius, start_angle, span, offset, color='red').\
                draw_connecting_line(length, offset, color='red', ls='dashed')
            arc(center, radius, start_angle,  -span, offset, color='blue').\
                draw_connecting_line(length, offset, color='blue', ls='dashed')

    def test_connecting_arc(self):
        """
        """
        blueprint('Test connecting arcs', 'A4')
        p0 = Point()
        d = 50.
        r = 15.
        for angle in np.linspace(0., 360., 9):
            l = line(p0, p0.move(d, angle))
            l.draw_connecting_arc(r, 90.)
            l.draw_connecting_arc(r, -90.)

    def test_caps(self):
        """
        """
        blueprint('Test caps', 'A4')
        start_point = Point(0., 0.)
        base = 50.
        height = 25.
        corner_radius = 2.5
        offset = Point(-50., 50.)
        start_point.draw(offset)
        ccap(start_point, base, height, corner_radius, offset)
        offset = Point(-50., -75.)
        start_point.draw(offset)
        rccap(start_point, base, height, corner_radius, offset)
        offset = Point(50., 50.)
        start_point.draw(offset)
        ucap(start_point, base, height, corner_radius, offset)
        offset = Point(50., -50.)
        start_point.draw(offset)
        rucap(start_point, base, height, corner_radius, offset)

    def test_drawables(self):
        """
        """
        drawables = [
            Point(),
            Line(Point(-10., -10.), Point(10., 10)),
            Rectangle(Point(0., 0.), 50., 20., 2.5),
            Circle(Point(0., 0.), 25.),
            Cap(Point(0., 0.), 90., 50., 20., 2.5),
            Cross(Point(0., 0.), 25.),
            Hole(Point(0., 0.), 25.),
            ]
        offsets = [Point(), Point(50., 50.), Point(-50., -50.)]
        for drawable in drawables:
            blueprint(f'Test {drawable.__class__.__name__}', 'A4')
            for offset in offsets:
                drawable.draw(offset)




if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
