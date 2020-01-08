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


"""Test suite for the blueprint module.
"""

import unittest
import sys

from metalute.blueprint import blueprint
from metalute.matplotlib_ import plt
if sys.flags.interactive:
    plt.ion()


class TestBlueprint(unittest.TestCase):

    """Unit tests for the blueprint module.
    """

    def test_a4(self) -> None:
        """Test a plain a4 blueprint.
        """
        blue = blueprint('Test blueprint', 'A4')



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
