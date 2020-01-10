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

"""Dimensioning facilities.
"""

from metalute.geometry import Point, Line, CircleArc
from metalute.matplotlib_ import plt


class Arrow(Line):

    """
    """

    def draw(self, head_radius: float = 1.5, **fmt):
        """
        """
        super().draw(**fmt)
        phi = self.slope() + 90.
        p = self.p2.move(head_radius, phi)
        CircleArc(p, head_radius, phi + 90., phi + 180.).draw(full_circle=False, radii=False, **fmt)
        phi -= 180.
        p = self.p2.move(head_radius, phi)
        CircleArc(p, head_radius, phi - 180., phi - 90.).draw(full_circle=False, radii=False, **fmt)



def dim(p1, p2, offset, padding: float = 3., distance: float = 15., margin: float = 5.):
    """
    """
    p1 += offset
    p2 += offset
    fmt = dict(offset=Point(0., 0.), color='lightgray')
    # Basic setup.
    line = Line(p1, p2)
    phi = line.slope() - 90.
    length = line.length()
    d = distance + margin
    # Draw the two lines from the original points defining the dimension.
    Line(p1.move(padding, phi), p1.move(d, phi)).draw(**fmt)
    Line(p2.move(padding, phi), p2.move(d, phi)).draw(**fmt)
    # Now the actual dimension.
    _p1 = p1.move(distance, phi)
    _p2 = p2.move(distance, phi)
    l = Line(_p1, _p2)
    m = l.midpoint()
    text = '{:.2f}'.format(length)
    rot = phi + 90.
    if rot < -90.:
        rot += 180.
    elif rot > 90:
        rot -= 180
    print(rot)
    plt.text(*m.xy(), text, rotation=rot, ha='center', va='center')
    _d = 1.2 * len(text)
    Arrow(m.move(_d, phi - 90.), _p1).draw(**fmt)
    Arrow(m.move(_d, phi + 90.), _p2).draw(**fmt)



def hdim(y, x1, x2, tick=2., va='top', pad=2., intent=None, text_size: int = 15):
    """
    """
    if va == 'bottom':
        pad = -pad
    fmt = dict(color='lightgrey')
    plt.hlines(y, x1, x2, **fmt)
    plt.vlines(x1, y - tick, y + tick, **fmt)
    plt.vlines(x2, y - tick, y + tick, **fmt)
    dist = abs(x2 - x1)
    txt = '{:.2f} mm'.format(dist)
    fmt = dict(size=text_size, ha='center', va=va)
    plt.text(0.5 * (x1 + x2), y - pad, txt, **fmt)


def vdim(x, y1, y2, tick=2., ha='left', pad=2., intent=None, text_size: int = 15):
    """
    """
    if ha == 'right':
        pad = -pad
    fmt = dict(color='lightgrey')
    plt.vlines(x, y1, y2, **fmt)
    plt.hlines(y1, x - tick, x + tick, **fmt)
    plt.hlines(y2, x - tick, x + tick, **fmt)
    dist = abs(y2 - y1)
    txt = '{:.2f} mm'.format(dist)
    fmt = dict(size=text_size, ha=ha, va='center', rotation=90.)
    plt.text(x + pad, 0.5 * (y1 + y2), txt, **fmt)
