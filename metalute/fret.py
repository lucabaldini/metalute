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

"""Freatboard-related facilities.
"""

from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt

from metalute.dimension import dim


@dataclass
class Fretboard:

    """Class representing a generic fretboard.

    The default values are (loosely) borrowed from the Ibanez JEM model, see
    https://www.ibanez.com/usa/products/detail/jem7v_12.html
    but should only be used for making quick tests easier. All the lengths are
    in mm. Below are some notes on the nomenclature.

    The scale length or scale of a string instrument is the maximum vibrating
    length of the strings that produce sound, and determines the range of tones
    that a string can produce at a given tension. It's also called string length.
    (Operationally, the scale length is measured by dubling the distance between
    the nut and the 12th fret.)
    The scale length of an electric guitar affects both its playability and its
    tone. Regarding playability, a shorter scale length allows more compact
    fingering and favors shorter fingers and hand-span. A longer scale allows
    more expanded finger and favors longer fingers and hand-span. With regard to
    tone, a longer scale favors "brightness" or cleaner overtones and more
    separated harmonics versus a shorter scale scale length), which favors
    "warmth" or more muddy overtones.
    Practical scale lengths range from 19.4 in (492 mm) to 30 in (762 mm), with
    the "standard" Fender stratocaster sitting at 25.5 in (648 mm).
    """

    num_frets: int = 24
    reference_fret: int = 24
    scale_length: float = 648.
    nut_padding: float = 15.
    bridge_padding: float = 10.
    thickness: float = 15.
    radius: float = 430.
    width_at_nut: float = 43.
    width_at_reference_fret: float = 58.

    def __post_init__(self):
        """Post-initialization code.
        """
        self.fret_grid = Fretboard.build_fret_grid(self.num_frets, self.scale_length)
        self.width_slope = (self.width_at_reference_fret - self.width_at_nut) /\
                           self.fret_distance_to_nut(self.reference_fret)

    @staticmethod
    def build_fret_grid(num_frets: int, scale_length: float):
        """Calculate the array of distances of the frets from the nut for a
        given freatboard configuration (i.e., scale length and number of frets).

        The basic equation relating the fundamental quantities at play for a
        vibrating string is

        f = \\frac{1}{2L} \\sqrt{\\frac{T}{\\varrho}}

        where f is the frequency of the note, L is the length of the string, T
        is the tension and \\varrho the string mass per unit length.

        From the standpoint of calculating the fret position the only thing that
        we care about is pretty much the fact that, all the rest being unchanged,
        the pitch of the note is inversely proportional to the length. Since the
        distance s, measured in semitones, between two frequencies f1 and f2 is

        s(f_1, f_2) = 12 \\log_2(\\frac{f_2}{f_1})

        d_i = L(1 - 2^{-\\frac{i}{2}})
        """
        return scale_length * (1. - 2. ** (-np.arange(1, num_frets + 1) / 12.))

    def fret_distance_to_nut(self, fret: int):
        """Return the overall distance between a given fret and the guitar nut.
        """
        return self.fret_grid[fret - 1]

    def total_length(self):
        """Return the total length of the fretboard, including the padding on
        both sides.
        """
        return self.fret_distance_to_nut(self.num_frets) + self.bridge_padding

    def width(self, dist_from_nut):
        """
        """
        return self.width_at_nut + self.width_slope * dist_from_nut

    def width_at_half_scale(self):
        """
        """
        pass

    def width_at_bridge(self):
        """
        """
        pass

    def draw_top_shape(self, position, axis: bool = False,
                       dimensioning: bool = False, **kwargs):
        """
        """
        kwargs.setdefault('color', 'black')
        x0, y0 = position
        l = self.total_length()
        w1 = 0.5 * self.width_at_nut
        w2 = 0.5 * self.width_at_reference_fret
        x = np.array([0., 0., -l, -l, 0.]) + x0
        y = np.array([-w1, w1, w2, -w2, -w1]) + y0
        plt.plot(x, y, **kwargs)
        if axis:
            plt.hlines(y0, x0, x0 -self.scale_length, ls='dashed', color='lightgray')
        if dimensioning:
            hdim(-w2 - 5., x0, x0 - self.fret_distance_to_nut(12))
            hdim(-w2 - 15., x0, x0 - l)
            #hdim(-w2 - 25., x0, x0 - self.scale_length)

    def draw_top_frets(self, position, indices: bool = True, **kwargs):
        """
        """
        x0, y0 = position
        x = -self.fret_grid + x0
        y = 0.5 * self.width(self.fret_grid) + y0
        plt.vlines(x, -y, y)
        if indices:
            fmt = dict(size=15, ha='center', va='center')
            _y = y.max() + 6.
            for i, _x, in enumerate(x):
                plt.text(_x, _y, '{}'.format(i + 1), **fmt)
                circle = plt.Circle((_x, _y), radius=4., fill=False)
                plt.gca().add_patch(circle)

    def draw_bridge_reference(self, position):
        """
        """
        x0, y0 = position
        x = x0 - self.scale_length
        y = 80.
        plt.vlines(x, -y, y)

    def draw(self, position=(0., 0)):
        """
        """
        fmt = dict(color='black')
        self.draw_top_shape(position, **fmt)
        self.draw_top_frets(position, **fmt)




class ScaleLength:

    """Remove me.
    """

    # Brian May's Red Special, along with Fender Jaguar and Mustang.
    RedSpecial = 610.
    # Most Gretsch guitars.
    Gretsch = 625.
    # Most Gibson guitars, including Les Paul and SG.
    Gibson = 628.
    # Most Paul Red Smith guitars.
    PaulRedSmith = 635.
    # Most Fender, Ibanez and Jackson.
    Standard = 648.
