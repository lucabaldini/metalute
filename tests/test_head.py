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

from metalute.head import StratoHeadstock
from metalute.matplotlib_ import plt, drafting_figure
from metalute.geometry import Point
from metalute.units import inches_to_mm
from metalute import TEST_DATA_FOLDER
#if sys.flags.interactive:
#    plt.ion()



class TestHead(unittest.TestCase):

    """Unit tests for the head module.
    """

    def load_strato_data(self):
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

    def test_strato(self) -> None:
        """.
        """
        drafting_figure('Stratocaster headstock', 'A4')
        headstock = StratoHeadstock()
        offset = Point(-80., 10.)
        headstock.draw_top(offset)

    def test_strato_construction(self) -> None:
        """.
        """
        drafting_figure('Stratocaster headstock construction', 'A4')
        headstock = StratoHeadstock()
        offset = Point(-80., 10.)
        headstock.draw_top(offset, points=True, construction=True)

    def test_strato_accuracy(self) -> None:
        """
        """
        drafting_figure('Stratocaster headstock accuracy', 'A4')
        headstock = StratoHeadstock()
        offset = Point(-80., 10.)
        headstock.draw_top(offset)
        x, y, xh, yh = self.load_strato_data()
        x += offset.x
        y += offset.y
        plt.plot(x, y, 'o')
        xh += offset.x
        yh += offset.y
        print(xh, yh)
        plt.plot(xh, yh, 'o')



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
    if sys.flags.interactive:
        plt.show()
