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

"""Geometry-related facilities.
"""

from string import ascii_uppercase

# We have to sort this out---the default is not working on my Fedora 30.
import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt

from metalute.units import mm_to_inches


def rectangle(width: float, height: float, center=(0., 0.), **kwargs):
    """Draw a rectangle with specified width, height and center.
    """
    x, y = center
    x -= width / 2.
    y -= height / 2.
    pos = (x, y)
    patch = matplotlib.patches.Rectangle(pos, width, height, fill=False, **kwargs)
    plt.gca().add_patch(patch)


def technical_grid(width: float, height: float, margin: float, xdiv: int, ydiv: int):
    """
    """
    l = margin / 2.
    x0 = width / 2. - margin
    y0 = height / 2. - margin
    x = np.linspace(-x0, x0, xdiv + 1)
    y = np.linspace(-y0, y0, ydiv + 1)
    # Draw the small lines on the edges.
    plt.hlines(y, -x0, -x0 - l)
    plt.hlines(y, x0, x0 + l)
    plt.vlines(x, -y0, -y0 - l)
    plt.vlines(x, y0, y0 + l)
    # Draw the letter and numbers.
    dx = x0 / xdiv
    dy = y0 / ydiv
    fmt = dict(size=25, ha='center', va='center')
    for i, _x in enumerate(np.flip((x + dx)[:-1])):
        plt.text(_x, -y0 - l, '{}'.format(i + 1), **fmt)
        plt.text(_x, y0 + l, '{}'.format(i + 1), rotation=90., **fmt)
    for i, _y in enumerate((y + dy)[:-1]):
        plt.text(-x0 - l, _y, '{}'.format(ascii_uppercase[i]), **fmt)
        plt.text(x0 + l, _y, '{}'.format(ascii_uppercase[i]), rotation=90., **fmt)


def technical_figure(figure_name: str, width: float, height: float,
                     margin: float, xdiv: int, ydiv: int):
    """
    """
    plt.figure(figure_name)
    plt.gcf().set_size_inches(mm_to_inches(width), mm_to_inches(height))
    plt.gca().set_aspect('equal')
    plt.gca().axis([-width / 2., width / 2., -height / 2., height / 2.])
    plt.subplots_adjust(left=-0.0001, right=1.0001, top=1.0001, bottom=0.)
    w = width - 2. * margin
    h = height - 2. * margin
    rectangle(w, h)
    technical_grid(width, height, margin, xdiv, ydiv)


def a0figure(figure_name: str):
    """
    """
    technical_figure(figure_name, 1189., 841., 30., 16, 12)



if __name__ == '__main__':
    a0figure('Test figure')
    plt.hlines(0, 0, 500)
    plt.savefig('test.pdf')
