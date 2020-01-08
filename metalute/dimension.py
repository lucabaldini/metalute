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
