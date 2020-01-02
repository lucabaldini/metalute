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

"""matplotlib configuration.
"""

from string import ascii_uppercase

import numpy as np
from matplotlib import pyplot as plt
import matplotlib
# We have to sort this out---the default is not working on my Fedora 30.
matplotlib.use('TkAgg')

from metalute.units import mm_to_inches


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


def _set(key, value):
    """Set a specific parameter to a given value.
    """
    matplotlib.rcParams[key] = value


def _get(key):
    """Retrieve the value of a given parameter.
    """
    return matplotlib.rcParams[key]


def mm_to_points(mm: float, ppi: float = 72.):
    """Convert a physical length (in mm) to points.

    Mind that ppi is not the same thing as dpi, see
    https://stackoverflow.com/questions/47633546
    """
    return ppi * mm_to_inches(mm)


def setup_page(size: str, orientation: str = 'Landscape', dpi: float = 100.,
               text_size: float = 3., line_width: float = 0.25):
    """Basic figure setup for a given paper size.
    """
    assert orientation in PAPER_ORIENTATIONS
    width, height = PAPER_SIZE_DICT[size]
    if orientation == 'Landscape':
        width, height = height, width
    # Set the page size and resolution.
    _set('figure.figsize', (mm_to_inches(width), mm_to_inches(height)))
    _set('figure.dpi', dpi)
    # Set the text size.
    _set('font.size', mm_to_points(text_size))
    # Set the line width.
    lw = mm_to_points(line_width)
    _set('lines.linewidth', lw)
    _set('patch.linewidth', lw)
    return width, height, dpi


def drafting_figure(name: str, size: str, orientation: str = 'Landscape',
                    dpi: float = 100., text_size: float = 3.,
                    line_width: float = 0.25, margin: float = 0.05,
                    pitch: float = 30., tick_size: float = 7.5):
    """Create a custom figure for techical drawings.
    """
    # Setup the page.
    width, height, dpi = setup_page(size, orientation, dpi, text_size, line_width)
    # Create an empty figure.
    plt.figure()
    # Setup the axes.
    plt.gca().set_aspect('equal')
    plt.gca().axis([-0.5 * width, 0.5 * width, -0.5 * height, 0.5 * height])
    plt.subplots_adjust(left=-0.0001, right=1.0001, top=1.0001, bottom=0.)
    plt.xticks([])
    plt.yticks([])
    # Draw a rectangle delimiting the drafting area.
    margin *= max(width, height)
    w = width - 2. * margin
    h = height - 2. * margin
    hw = 0.5 * w
    hh = 0.5 * h
    kwargs = dict(fill=False)
    patch = matplotlib.patches.Rectangle((-hw, -hh), w, h, **kwargs)
    plt.gca().add_patch(patch)
    # Add the reference grid on the borders.
    nx = int(width / pitch + 0.5)
    ny = int(height / pitch + 0.5)
    x = np.linspace(-hw, hw, nx + 1)
    y = np.linspace(-hh, hh, ny + 1)
    plt.hlines(y, -hw, -hw - tick_size)
    plt.hlines(y, hw, hw + tick_size)
    plt.vlines(x, -hh, -hh - tick_size)
    plt.vlines(x, hh, hh + tick_size)
    # Add the letters and numbers to the reference grid.
    dx = hw / nx
    dy = hh / ny
    fmt = dict(size='large', ha='center', va='center')
    for i, _x in enumerate(np.flip((x + dx)[:-1])):
        plt.text(_x, -hh - tick_size, '{}'.format(i + 1), **fmt)
        plt.text(_x, hh + tick_size, '{}'.format(i + 1), rotation=90., **fmt)
    for i, _y in enumerate((y + dy)[:-1]):
        plt.text(-hw - tick_size, _y, '{}'.format(ascii_uppercase[i]), **fmt)
        plt.text(hw + tick_size, _y, '{}'.format(ascii_uppercase[i]), rotation=90., **fmt)



if __name__ == '__main__':
    drafting_figure('Test figure', 'A3')
    plt.hlines(0., 0., 10.)
    plt.vlines(10., 10., 13.)
    plt.text(10., 10., 'Hello!')
    plt.savefig('draft.pdf')
    plt.show()
