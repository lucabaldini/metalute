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

from metalute.head import FenderHeadstock
from metalute.matplotlib_ import plt, drafting_figure
from metalute.geometry import Point
from metalute.units import inches_to_mm
from metalute import TEST_DATA_FOLDER
#if sys.flags.interactive:
#    plt.ion()



class TestHead(unittest.TestCase):

    """Unit tests for the head module.
    """

    def load_fender_data(self):
        """
        """
        file_path = os.path.join(TEST_DATA_FOLDER, 'headstock_fender_profile.txt')
        x, y = np.loadtxt(file_path, unpack=True, delimiter=',')
        x -= x.min()
        scale = x.max() / inches_to_mm(7.313)
        x /= scale
        y /= -scale
        y -= 0.5 * (y[0] + y[-1])
        return x, y

    def test_fender_construction(self) -> None:
        """.
        """
        drafting_figure('Fender headstock construction', 'A4')
        headstock = FenderHeadstock()
        offset = Point(-80., 10.)
        headstock.draw_top(offset, points=True, construction=True)

    def test_fender_accuracy(self) -> None:
        """
        """
        drafting_figure('Fender headstock accuracy', 'A4')
        headstock = FenderHeadstock()
        offset = Point(-80., 10.)
        headstock.draw_top(offset)
        x, y = self.load_fender_data()
        x += offset.x
        y += offset.y
        plt.plot(x, y, 'o')



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
    if sys.flags.interactive:
        plt.show()
