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

from enum import Enum

import numpy as np


class ScaleLength(Enum):

    """Scale length (in mm) for some relevant electric guitars.

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



class Fretboard:

    """Class representing a guitar/bass freatboard.
    """

    def __init__(self, scale_length: float, num_frets: int, width: float = 60.,
                 thickness: float = 12., radius: float = 50.) -> None:
        """Constructor.
        """
        self.scale_length = scale_length
        self.num_frets = num_frets
        self.width = width
        self.thickness = thickness
        self.radius = radius
        self.fret_positions = Fretboard.calculate_fret_positions(scale_length, num_frets)

    @staticmethod
    def calculate_fret_positions(scale_length: float, num_frets: int):
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

    def fret_spacing(self):
        """Return the array of fret spacing values.

        Note that 0. is prepended to the array of positions beforehand, so that
        the fret spacing array has the same dimension of the fret positions,
        and the first value is the distance of the first fret from the nut.
        """
        return np.diff(self.fret_positions, prepend=0.)

    def draw(self):
        """
        """
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        plt.figure()
        plt.gca().set_aspect('equal')
        plt.gca().axis([0, 700, -350, 350])
        plt.vlines(self.fret_positions, -10, 10)
