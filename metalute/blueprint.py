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

import time
from string import ascii_uppercase

import numpy as np
from matplotlib.offsetbox import TextArea, VPacker, AnchoredOffsetbox

from metalute.matplotlib_ import plt, setup_page, mm_to_points


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



class MultiTextBox(AnchoredOffsetbox):

    """
    """

    def __init__(self, fields):
        """
        """
        lines = []
        for key, value in fields.items():
            lines.append(TextArea(key.upper(), textprops={'color': 'lightgray'}))
            lines.append(TextArea('    {}                       '.format(value)))
        pack = VPacker(children=lines, pad=0., sep=2.)
        super().__init__(4, child=pack, borderpad=0.)
        plt.gca().add_artist(self)



class BlueprintBox(MultiTextBox):

    """
    """

    def __init__(self, title, author):
        """
        """
        fields = dict(title=title, author=author, date=time.asctime())
        super().__init__(fields)



def hruler(y, xmin, xmax, step=10., line_width=0.15):
    """
    """
    fmt = dict(lw=mm_to_points(line_width))
    plt.hlines(y, xmin, xmax, **fmt)
    x = np.arange(xmin, xmax + 0.5 * step, step)
    plt.vlines(x, y, y - 2., **fmt)
    fmt = dict(size='small', ha='center', va='top')
    for _x in x:
        text = '{:.0f}'.format(_x)
        if text == '0':
            text += ' mm'
        plt.text(_x, y - 3., text, **fmt)



def vruler(x, ymin, ymax, step=10., line_width=0.15):
    """
    """
    fmt = dict(lw=mm_to_points(line_width))
    plt.vlines(x, ymin, ymax, **fmt)
    y = np.arange(ymin, ymax + 0.5 * step, step)
    plt.hlines(y, x, x + 2., **fmt)
    fmt = dict(size='small', ha='left', va='center')
    for _y in y:
        text = '{:.0f}'.format(_y)
        if text == '0':
            text += ' mm'
        plt.text(x + 3, _y, text, **fmt)


def blueprint(name: str, size: str, author=None, orientation: str = 'Landscape',
              dpi: float = 100., text_size: float = 3., line_width: float = 0.25,
              margin: float = 0.05, pitch: float = 30., tick_size: float = 7.5):
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
    delta = 5.
    span = 0.75
    l = 10 * int((span * w) / 10.)
    hruler(h - delta, -l, l)
    l = 10 * int((span * h) / 10.)
    vruler(-w + delta, -l, l)
    box = BlueprintBox(name, author)
