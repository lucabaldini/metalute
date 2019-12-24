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
from metalute.units import inches_to_mm, mm_to_inches



class TestUnits(unittest.TestCase):

    """Unit tests for the units module.
    """

    def test_simple(self) -> None:
        """Basic test.
        """
        self.assertAlmostEqual(inches_to_mm(1.), 25.4)
        self.assertAlmostEqual(mm_to_inches(1.), 0.0393701)

    def test_roundtrip(self, value: float = 648.) -> None:
        """Test roundtrip.
        """
        self.assertAlmostEqual(inches_to_mm(mm_to_inches(value)), value)



if __name__ == '__main__':
    unittest.main()
