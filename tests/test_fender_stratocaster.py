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
import os

import numpy as np
from scipy.optimize import curve_fit

from metalute.fit import fit_circle_arc
from metalute.head import FenderStratocasterContour, FenderStratocaster
from metalute.geometry import Point, Circle, CircularArc, Line
from metalute.matplotlib_ import plt
from metalute.blueprint import blueprint
from metalute.geometry import Point
from metalute.units import inches_to_mm
from metalute import TEST_DATA_FOLDER
if sys.flags.interactive:
    plt.ion()



class TestFenderStratocaster(unittest.TestCase):

    """Unit tests for the head module.
    """

    def load_data(self):
        """
        """
        file_path = os.path.join(TEST_DATA_FOLDER, 'headstock_fender_profile.txt')
        x, y = np.loadtxt(file_path, unpack=True, delimiter=',')
        scale = (x.max() - x.min()) / inches_to_mm(7.313)
        xoffset = x.min()
        yoffset = 0.5 * (y[0] + y[-1])

        def to_physical_coordinates(x, y):
            """
            """
            return (x - xoffset) / scale, -(y - yoffset) / scale

        x, y = to_physical_coordinates(x, y)

        file_path = os.path.join(TEST_DATA_FOLDER, 'headstock_fender_holes.txt')
        xh, yh = np.loadtxt(file_path, unpack=True, delimiter=',')
        xh, yh = to_physical_coordinates(xh, yh)
        return x, y, xh, yh

    def test_accuracy(self):
        """
        """
        blueprint('Fender Stratocaster accuracy', 'A4')
        x, y, xh, yh = self.load_data()
        offset = Point(-80., 0.)
        plt.plot(x + offset.x, y + offset.y, 'o')
        head = FenderStratocasterContour()
        head.draw(offset)

    def test_draw(self):
        """
        """
        blueprint('Fender Stratocaster', 'A4')
        offset = Point(-80., 0.)
        head = FenderStratocaster()
        head.contour.draw_construction(offset)
        head.draw_top(offset)
        head.dimension_top(offset)
        head.contour.draw_reference_points(offset)



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
