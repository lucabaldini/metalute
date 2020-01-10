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

from metalute.geometry import Point, plt
from metalute.dimension import dim
from metalute.blueprint import blueprint
if sys.flags.interactive:
    plt.ion()


class TestDimension(unittest.TestCase):

    """Unit tests for the geometry module.
    """

    def test_point(self) -> None:
        """Test the Point class.
        """
        offset = Point(0., 0.)
        p1 = Point(0., 0., 'p1')
        p2 = Point(0., 50., 'p2')
        p3 = Point(-50., -50., 'p2')
        p4 = Point(50., 50., 'p4')
        p5 = Point(100., 50., 'p5')
        blueprint('Test dimensioning', 'A4')
        p1.draw(offset)
        p2.draw(offset)
        p3.draw(offset)
        p4.draw(offset)
        p5.draw(offset)
        dim(p1, p2, offset)
        dim(p1, p3, offset)
        dim(p3, p1, offset)
        dim(p4, p5, offset)


if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
