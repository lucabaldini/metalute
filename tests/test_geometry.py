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

"""Test suite for the units module.
"""

import unittest
import sys

from metalute.blueprint import blueprint
from metalute.geometry import Point, Line, CircularArc, ParametricPolyPathBase
from metalute.matplotlib_ import plt
if sys.flags.interactive:
    plt.ion()


class TestGeometry(unittest.TestCase):

    """Unit tests for the geometry module.
    """

    def __test_point(self) -> None:
        """Test the Point class.
        """
        p0 = Point(0., 0.)
        p1 = Point(1., 1., 'p1')
        p2 = Point(2., 2., 'p2')
        print(p0)
        print(p1)
        print(p2)
        plt.figure('Drawing points')
        p0.draw()
        p1.draw()
        p2.draw()

    def _test_circular_arc_base(self, center, radius, start_phi, span, offset, **kwargs):
        """
        """
        arc = CircularArc(center, radius, start_phi, span)
        print(arc)
        arc.draw_construction(offset)
        arc.draw(offset, **kwargs)
        p1 = arc.start_point('p1')
        p2 = arc.end_point('p2')
        p1.draw(offset, **kwargs)
        p2.draw(offset, **kwargs)
        arc.connecting_line(10.).draw(offset, **kwargs)
        arc.connecting_circular_arc(5., 180.).draw(offset, **kwargs)
        kwargs['ls'] = 'dashed'
        arc.connecting_circular_arc(-5., 180.).draw(offset, **kwargs)
        return arc

    def test_circular_arc(self) -> None:
        """Test the circular arc class.
        """
        blueprint('Test CircularArc', 'A4')
        offset = Point(0., 0.)
        c1 = Point(0., 0., 'c1')
        arc1 = self._test_circular_arc_base(c1, 20., 0., 90., offset)
        c2 = Point(40., 40., 'c2')
        arc2 = self._test_circular_arc_base(c2, 30, 0., -90., offset, color='red')
        c3 = Point(-40., -40., 'c3')
        arc3 = self._test_circular_arc_base(c3, 25, 180., 90., offset, color='blue')
        c4 = Point(-40., 40., 'c4')
        arc4 = self._test_circular_arc_base(c4, 15, 180., -90., offset)

    def test_poly_path(self):
        """
        """
        blueprint('Test ParametricPolyPath', 'A4')
        offset = Point(0., 0.)

        class Pillow(ParametricPolyPathBase):

            DEFAULT_PAR_DICT = dict(width=75., height=25.)

            def construct(self):
                """
                """
                hw = 0.5 * self.width
                hh = 0.5 * self.height
                p = Point(-hw, hh)
                top = Line(p, p.move(self.width, 0.))
                c = top.p2.move(hh, -90.)
                right = CircularArc(c, hh, 90., -180.)
                bot = right.connecting_line(self.width)
                left = CircularArc(c.move(self.width, 180.), hh, -90., -180.)
                return locals()

        p = Pillow()
        p.draw_construction(offset)
        p.draw(offset)
        p.draw_reference_points(offset)



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
