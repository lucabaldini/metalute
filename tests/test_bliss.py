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


from metalute.head import BlissContour, MusicManContour
from metalute.geometry import Point
from metalute.blueprint import blueprint
from metalute.matplotlib_ import plt
if sys.flags.interactive:
    plt.ion()



class TestBliss(unittest.TestCase):

    """Unit tests for the head module.
    """

    def test(self):
        """
        """
        offset = Point(-80., 0.)
        blueprint('Bliss---cool, eh?', 'A4')
        head = BlissContour()
        head.draw_construction(offset)
        head.draw(offset)
        head.draw_reference_points(offset)
        MusicManContour().draw(offset, color='lightgray')
        blueprint('Bliss simplified', 'A4')
        head.draw(offset)



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
