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
from metalute.head import StratoHeadstock
from metalute.body import MusicManAxis
from metalute.geometry import Point, Circle, CircleArc, Line
from metalute.matplotlib_ import plt
from metalute.blueprint import blueprint
from metalute.geometry import Point
from metalute.units import inches_to_mm
from metalute import TEST_DATA_FOLDER
if sys.flags.interactive:
    plt.ion()



class TestHead(unittest.TestCase):

    """Unit tests for the head module.
    """

    def load_data(self):
        """
        """
        file_path = os.path.join(TEST_DATA_FOLDER, 'music_man_axis_body.txt')
        x, y = np.loadtxt(file_path, unpack=True, delimiter=',')
        scale = (993.8586723768738 - 174.64239828693792) / 648.
        xoffset = x[0]
        yoffset = y[0]

        def to_physical_coordinates(x, y):
            """
            """
            return (x - xoffset) / scale, -(y - yoffset) / scale

        x, y = to_physical_coordinates(x, y)
        return x, y

    def test_accuracy(self):
        """
        """
        blueprint('Music Man Axis accuracy', 'A1')
        offset = Point(-200., -50.)
        x, y = self.load_data()
        plt.plot(x + offset.x, y + offset.y, 'o')
        body = MusicManAxis()
        body.draw(offset)
        #fit_circle_arc(x, y, 13, 16).draw(offset)
        #fit_circle_arc(x, y, 18, 22, invert=True).draw(offset)
        #fit_circle_arc(x, y, 23, 26).draw(offset)
        #fit_circle_arc(x, y, 26, 29, invert=True).draw(offset)
        #fit_circle_arc(x, y, 29, 33, invert=True).draw(offset)
        #fit_circle_arc(x, y, 33, 37).draw(offset)
        #fit_circle_arc(x, y, 38, 42, invert=True).draw(offset)
        #fit_circle_arc(x, y, 42, 44, invert=True).draw(offset)
        #fit_circle_arc(x, y, 44, 47).draw(offset)

    def test_draw(self):
        """
        """
        blueprint('Music Man Axis', 'A1')
        offset = Point(-200., -50.)
        body = MusicManAxis()
        body.draw(offset)

    def _test_(self) -> None:
        """
        """
        blueprint('Music Man Axis', 'A2')
        offset = Point(-200., 0.)
        x, y = self.load_data()
        x += offset.x
        y += offset.y
        plt.plot(x, y, 'o')
        p0 = Point(0., 0., 'p0')
        #p0.draw(offset)

        def f(x, m, q, x0, gamma):
            return m * (1. - np.exp(-(x/x0)**gamma)) + q

        c1 = Point(240., 0.)
        n = 13
        _x = x[:n] - offset.x
        _y = y[:n] - offset.y
        #plt.plot(_x + offset.x, _y + offset.y)
        dx = _x - c1.x
        dy = _y - c1.y
        r = np.sqrt(dx**2. + dy**2.)
        theta = np.degrees(np.arctan2(dy, dx))
        print(theta)
        popt, pcov = curve_fit(f, theta, r, p0=(140., 100, 150., 5.))
        print(popt)
        grid = np.linspace(theta.min(), theta.max(), 250)
        theta = np.linspace(180., 100., 100)
        r = f(theta, *popt)
        x = c1.x + r * np.cos(np.radians(theta))
        y = c1.y + r * np.sin(np.radians(theta))
        plt.plot(x + offset.x, y + offset.y)
        plt.plot(x + offset.x, -y + offset.y)







if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
