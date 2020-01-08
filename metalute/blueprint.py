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

"""Blueprint.
"""

from string import ascii_uppercase

import numpy as np

from metalute.matplotlib_ import plt, setup_page


PAPER_SIZE_DICT = {'A0': (841., 1189.),
                   'A3': (297., 420.),
                   'A4': (210., 297),
                   'A5': (148., 210),
                   'US ANSI E': (864., 1118.),
                   'US ANSI B': (279., 432.),
                   'US Letter': (216., 279.),
                   'US Half Letter': (140., 216.)
                   }

PAPER_ORIENTATIONS = ['Portrait', 'Landscape']


def blueprint(name: str, size: str, orientation: str = 'Landscape', dpi: float = 100.,
              text_size: float = 3., line_width: float = 0.25, margin: float = 0.05,
              pitch: float = 30., tick_size: float = 7.5):
    """Create a custom figure for techical drawings.
    """
    assert orientation in PAPER_ORIENTATIONS
    width, height = PAPER_SIZE_DICT[size]
    if orientation == 'Landscape':
        width, height = height, width
    # Setup the page.
    width, height, dpi = setup_page((width, height), dpi, text_size, line_width)
    # Create an empty figure.
    plt.figure(name)
    # Setup the axes.
    plt.gca().set_aspect('equal')
    hmargin = margin
    vmargin = hmargin * width / height
    plt.subplots_adjust(left=hmargin, right=1. - hmargin, top=1. - vmargin, bottom=vmargin)
    plt.xticks([])
    plt.yticks([])
    w = 0.5 * width * (1. - 2. * hmargin)
    h = 0.5 * height * (1. - 2. * vmargin)
    plt.gca().axis([-w, w, -h, h])
    # Add the reference grid on the borders.
    nx = int(width / pitch + 0.5)
    ny = int(height / pitch + 0.5)
    x = np.linspace(-w, w, nx + 1)
    y = np.linspace(-h, h, ny + 1)
    plt.hlines(y, -w, -w - tick_size, clip_on=False)
    plt.hlines(y, w, w + tick_size, clip_on=False)
    plt.vlines(x, -h, -h - tick_size, clip_on=False)
    plt.vlines(x, h, h + tick_size, clip_on=False)
    # Add the letters and numbers to the reference grid.
    dx = w / nx
    dy = h / ny
    fmt = dict(size='large', ha='center', va='center')
    for i, _x in enumerate(np.flip((x + dx)[:-1])):
        plt.text(_x, -h - tick_size, '{}'.format(i + 1), **fmt)
        plt.text(_x, h + tick_size, '{}'.format(i + 1), rotation=90., **fmt)
    for i, _y in enumerate((y + dy)[:-1]):
        plt.text(-w - tick_size, _y, '{}'.format(ascii_uppercase[i]), **fmt)
        plt.text(w + tick_size, _y, '{}'.format(ascii_uppercase[i]), rotation=90., **fmt)
    # Add the reference rulers.
    delta = 8.
    span = 0.75
    x0, y0, l = 0., h - delta, 10 * int((span * w) / 10.)
    x = np.arange(-l, l + 0.5, 10.)
    plt.hlines(y0, -l, l)
    plt.vlines(x, y0, y0 - 2.)
    fmt = dict(size='small', ha='center', va='top')
    for _x in x:
        plt.text(_x, y0 - 3., '{:.0f}'.format(_x), **fmt)
    x0, y0, l = -w + delta, 0., 10 * int((span * h) / 10.)
    y = np.arange(-l, l + 0.5, 10.)
    plt.vlines(x0, -l, l)
    plt.hlines(y, x0, x0 + 2.)
    fmt = dict(size='small', ha='left', va='center')
    for _y in y:
        plt.text(x0 + 3., _y, '{:.0f}'.format(_y), **fmt)
