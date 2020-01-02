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

from metalute.geometry import Point, plt
if sys.flags.interactive:
    plt.ion()


class TestGeometry(unittest.TestCase):

    """Unit tests for the geometry module.
    """

    def test_point(self) -> None:
        """Test the Point class.
        """
        p0 = Point(0., 0.)
        p1 = Point(1., 1., 'p1')
        p2 = Point(2., 2., 'p2', 'test point')
        print(p0)
        print(p1)
        print(p2)
        plt.figure('Drawing points')
        p0.draw()
        p1.draw()
        p2.draw()



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
