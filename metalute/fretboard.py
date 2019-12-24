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

The scale length or scale of a string instrument is the maximum vibrating length
of the strings that produce sound, and determines the range of tones that
a string can produce at a given tension. It's also called string length.

(Operationally, the scale length is measured by dubling the distance between the
nut and the 12th fret.)

The scale length of an electric guitar affects both its playability and its
tone. Regarding playability, a shorter scale length allows more compact
fingering and favors shorter fingers and hand-span. A longer scale allows more
expanded finger and favors longer fingers and hand-span. With regard to tone, a
longer scale favors "brightness" or cleaner overtones and more separated
harmonics versus a shorter scale scale length), which favors "warmth" or more
muddy overtones.

Practical scale lengths range from 19.4 in (492 mm) to 30 in (762 mm), with the
"standard" Fender stratocaster sitting at 25.5 in (648 mm).
"""

from enum import Enum


class ScaleLength(Enum):

    """Scale length (in mm) for some relevant electric guitars.
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
