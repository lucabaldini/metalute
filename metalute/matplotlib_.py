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

import numpy as np
from matplotlib import pyplot as plt
import matplotlib
# We have to sort this out---the default is not working on my Fedora 30.
#matplotlib.use('TkAgg')

from metalute.units import mm_to_inches


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


def basic_setup():
    """System wide matplotlib configuration.
    """
    _set('lines.color', 'black')
    _set('patch.facecolor', 'black')


def setup_page(size, dpi: float = 100., text_size: float = 3., line_width: float = 0.25):
    """Basic figure setup for a given paper size.
    """
    width, height = size
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


# Apply the basic setup.
basic_setup()
