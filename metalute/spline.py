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

"""Spline facilities.
"""

import numpy as np
from scipy import interpolate
from scipy.interpolate import UnivariateSpline

from metalute.body import MusicManAxis as Body
from metalute.head import MusicMan as Head
from metalute.geometry import Point, Circle, CircularArc, Line
from metalute.matplotlib_ import plt
from metalute.blueprint import blueprint
from metalute.geometry import Point
from metalute.fret import Fretboard
from metalute.pickup import SingleCoilRouting, HumbuckerRouting


class ParametricSpline:

    """
    """

    def __init__(self, x, y, closed=True):
        """
        """
        self.x = x
        self.y = y
        if closed:
            self.x = np.append(self.x, self.x[0])
            self.y = np.append(self.y, self.y[0])
        self.tck, self.u = interpolate.splprep([self.x, self.y], s=0)

    def draw_points(self, offset, **kwargs):
        """
        """
        kwargs.setdefault('color', 'orange')
        plt.plot(self.x + offset.x, self.y + offset.y, 'x', **kwargs)

    def draw(self, offset, **kwargs):
        """
        """
        kwargs.setdefault('color', 'black')
        t = np.linspace(0., 1., 1000)
        x, y = interpolate.splev(t, self.tck)
        plt.plot(x + offset.x, y + offset.y, **kwargs)




def test_draw():
    """
    """
    blueprint('EJ #1', 'A1')
    offset = Point(-200., 0.)
    body = Body()
    #body.draw(offset)

    x = np.array([0., 15., 50., 125., 200., 230., 250., 280., 300., 325.,
                  350., 370., 385., 400., 405., 395., 384., 380.5, 379., 383., 393., 375., 354.,
                  340., 320., 305., 298.7, 315., 334.7, 325.8, 310., 266.,
                  230., 200., 120., 50., 10.])
    y = np.array([0., 80., 131., 160., 141.5, 124.3, 113.3, 106.4, 107.4, 115.,
                  123., 125.7, 123., 110.3, 90., 68., 57., 50., 42., 28., 10., -13.2, -27.5,
                  -28.58, -30.5, -40.5, -60., -90, -108.7, -122.5, -127.4, -115.1,
                  -116.2, -136., -159.4, -131., -69.])
    s = ParametricSpline(x, y)
    s.draw(offset)
    #s.draw_points(offset)

    p0 = Point(-50., 0)
    l = Line(p0, p0.move(500., 0.))
    l.draw(offset)

    fretboard = Fretboard(num_frets=22, reference_fret=22, width_at_nut=42.,
                          width_at_reference_fret=56., scale_length=648.)
    fretboard.draw_top_shape((590., 0.))
    fretboard.draw_top_frets((590., 0.), indices=False)
    fretboard.draw_bridge_reference((590., 0.))

    pickup = HumbuckerRouting()
    pickup.draw(Point(-10., 0.))

    pickup = SingleCoilRouting()
    pickup.draw(Point(80., 0.))




if __name__ == '__main__':
    test_draw()
    plt.show()
