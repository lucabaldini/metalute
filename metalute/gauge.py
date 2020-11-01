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

"""All about vibrating strings.
"""

import numpy


def vibrating_string_frequency(length, tension, linear_density):
    """Return the frequency of a vibrating string in Hz.

    Arguments
    ---------
    length : float
        The length of the string in mm

    tension : float
        The tension of the string in N

    linear_density : float
        The linear density of the string in kg/m
    """
    return 0.001 / (2. * length) * numpy.sqrt(tension / linear_density)



class StringGauge:

    EXTRA_SUPER_LIGHT = [.008, .010, .015, .021, .030, .038]
    LIGHT = [.009, .011, .016, .024, .032, .042]
    LIGHT_REGULAR = [.009, .011, .016, .026, .036, .046]
    REGULAR = [.010, .013, .017, .026, .036, .046]
    REGULAR_HEAVY = [.010, .013, .017, .032, .042, .052]
    MEDIUM = [.011, .014, .018, .028, .038, .049]
    HEAVY = [.012, .016, .024, .032, .042, .052]
