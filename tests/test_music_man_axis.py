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

from metalute.fit import fit_circle_arc, fit_line
from metalute.body import MusicManAxis as Body
from metalute.head import MusicMan as Head
from metalute.geometry import Point, Circle, CircularArc, Line
from metalute.matplotlib_ import plt
from metalute.blueprint import blueprint, hruler
from metalute.geometry import Point
from metalute.units import inches_to_mm
from metalute import TEST_DATA_FOLDER
if sys.flags.interactive:
    plt.ion()



class TestMusicManAxis(unittest.TestCase):

    """Unit tests for the head module.
    """

    @classmethod
    def setUpClass(cls):
        """Load the necessary data.
        """
        cls.xb, cls.yb, cls.xh, cls.yh = cls._load_data()

    @staticmethod
    def _load_data():
        """Load the input data.
        """
        # Read the input file with the body data.
        file_path = os.path.join(TEST_DATA_FOLDER, 'music_man_axis_body.txt')
        x, y = np.loadtxt(file_path, unpack=True, delimiter=',')
        # The conversion factor to physical units are taken by imposing that
        # the scale length of the guitar on the original image is the nominal one.
        scale = (993.8586723768738 - 174.64239828693792) / 648.
        # Body coordinates.
        xoffset = x[0]
        yoffset = y[0]
        xb, yb = (x - x[0]) / scale, -(y - y[0]) / scale
        # And now off to the headstock.
        file_path = os.path.join(TEST_DATA_FOLDER, 'music_man_axis_headstock.txt')
        x, y = np.loadtxt(file_path, unpack=True, delimiter=',')
        # Mind we take the seventh to last point here because it represents the
        # anchor, and the following 6 ones are the holes.
        xh, yh = (x - x[-7]) / scale, -(y - y[-7]) / scale
        return xb, yb, xh, yh

    def fit_body(self):
        """
        """
        fit_circle_arc(self.xb, self.yb, 13, 16).draw(offset)
        fit_circle_arc(self.xb, self.yb, 18, 22, invert=True).draw(offset)
        fit_circle_arc(self.xb, self.yb, 23, 26).draw(offset)
        fit_circle_arc(self.xb, self.yb, 26, 29, invert=True).draw(offset)
        fit_circle_arc(self.xb, self.yb, 29, 33, invert=True).draw(offset)
        fit_circle_arc(self.xb, self.yb, 33, 37).draw(offset)
        fit_circle_arc(self.xb, self.yb, 38, 42, invert=True).draw(offset)
        fit_circle_arc(self.xb, self.yb, 42, 44, invert=True).draw(offset)
        fit_circle_arc(self.xb, self.yb, 44, 47).draw(offset)

    def test_body_accuracy(self):
        """
        """
        blueprint('Music Man Axis body accuracy', 'A1')
        offset = Point(-200., -50.)
        plt.plot(self.xb + offset.x, self.yb + offset.y, 'o')
        body = Body()
        body.draw(offset)

    def test_body_draw(self):
        """
        """
        blueprint('Music Man Axis', 'A1')
        offset = Point(-200., -50.)
        body = Body()
        body.draw_construction(offset)
        body.draw(offset)
        body.draw_reference_points(offset)

    def test_body_draw_split(self):
        """
        """
        x0 = 200.
        y0 = 0.
        blueprint('Music Man Axis 1', 'A3', orientation='Portrait')
        offset = Point(-100., 15.)
        plt.hlines(y0, -1000., 1000.)
        plt.vlines(x0 + offset.x, -1000., 1000.)
        body = Body()
        body.draw_construction(offset)
        body.draw(offset)
        body.draw_reference_points(offset)
        plt.savefig('axis1.pdf')
        blueprint('Music Man Axis 2', 'A3', orientation='Portrait')
        offset = Point(-300., 15.)
        plt.hlines(y0, -1000., 1000.)
        plt.vlines(x0 + offset.x, -1000., 1000.)
        body = Body()
        body.draw_construction(offset)
        body.draw(offset)
        body.draw_reference_points(offset)
        plt.savefig('axis2.pdf')

    def fit_head(self):
        """
        """
        #fit_circle_arc(self.xh, self.yh, 13, 20).draw(offset)
        #fit_circle_arc(self.xh, self.yh, 20, 24).draw(offset)
        #fit_circle_arc(self.xh, self.yh, 25, 29).draw(offset)
        #fit_line(self.xh, self.yh, 7, 13).draw(offset, color='red')
        #fit_line(self.xh, self.yh, -6, -3).draw(offset, color='red')
        #fit_line(self.xh, self.yh, -2, len(self.xh)).draw(offset, color='red')

    def test_head_accuracy(self):
        """
        """
        blueprint('Music Man Axis head accuracy', 'A4')
        offset = Point(-60., 0.)
        plt.plot(self.xh + offset.x, self.yh + offset.y, 'o')
        head = Head()
        head.draw_top(offset)

    def test_head_draw(self):
        """
        """
        blueprint('Music Man Axis head', 'A4')
        offset = Point(-60., 0.)
        head = Head()
        head.contour.draw_construction(offset)
        head.draw_top(offset)
        head.contour.draw_reference_points(offset)



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
