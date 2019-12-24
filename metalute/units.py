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

"""Unit conversions.
"""

# Definition of an inch, see https://en.wikipedia.org/wiki/Inch
MM_PER_INCHES = 25.4


def inches_to_mm(inches: float) -> float:
    """Convert inches to mm.
    """
    return inches * MM_PER_INCHES


def mm_to_inches(mm: float) -> float:
    """Convert mm to inches.
    """
    return mm / MM_PER_INCHES
