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

"""Test suite for the freatboard module.
"""

import unittest

import numpy as np

from metalute.fretboard import Fretboard


# Test run from https://www.stewmac.com/FretCalculator.html with 648.000 mm
# length scale.
TEST_DATA = [36.369,
             70.698,
             103.099,
             133.682,
             162.549,
             189.795,
             215.512,
             239.786,
             262.697,
             284.322,
             304.734,
             324.000,
             342.185,
             359.349,
             375.550,
             390.841,
             405.274,
             418.897,
             431.756,
             443.893,
             455.348,
             466.161,
             476.367,
             486.000]


class TestFretboard(unittest.TestCase):

    """Unit tests for the fretboard module.
    """

    @classmethod
    def setUpClass(cls):
        """Create the fretboard for the test.
        """
        cls.fretboard = Fretboard(648., 24)

    def test_fret_positions(self) -> None:
        """Make sure our calculation of the fret position matches the online
        tool at https://www.stewmac.com/FretCalculator.html
        """
        self.assertTrue(np.allclose(self.fretboard.fret_positions, TEST_DATA, rtol=2.e-5))

    def test_fret_spacing(self) -> None:
        """Make sure that the ratio between the spacing among adjacent frets is
        equal to the magic number 2.**(1. / 12.).
        """
        spacing = self.fretboard.fret_spacing()
        ratio = spacing[:-1] / spacing[1:]
        self.assertTrue(np.allclose(ratio, 2.**(1. / 12.)))



if __name__ == '__main__':
    unittest.main()
