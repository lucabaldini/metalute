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
import pandas as pd

from metalute.units import inches_to_mm, newton_to_pounds
from metalute.pitch import GUITAR_STANDARD_TUNING


# Desity of the stainless steel in kg/m^3
STAINLESS_STEEL_DENSITY = 7.85e3


def vibrating_string_frequency(length, tension, linear_density):
    """Return the frequency of a vibrating string in Hz.

    Arguments
    ---------
    length : float
        The length of the string in mm

    tension : float
        The tension of the string in N

    linear_density : float
        The linear density of the string in kg/mm
    """
    return 1. / (2. * length) * numpy.sqrt(tension / linear_density)


def string_tension(length, diameter, frequency, density=STAINLESS_STEEL_DENSITY):
    """
    """
    linear_density = 1.e-12 * density * numpy.pi * inches_to_mm(diameter)**2 / 4.
    return 4. * length**2. * frequency**2. * linear_density




class StringGauge:

    """Class describing a string gauge.

    Arguments
    ---------
    diameters : array_like
        The string diameters in inches.
    """

    def __init__(self, name, diameters):
        """Constructor.
        """
        self.name = name
        self.diameters = numpy.array(diameters, dtype=float)

    def tensions(self, scale_length, tuning=GUITAR_STANDARD_TUNING):
        """Return the tensions of the strings in N.
        """
        return string_tension(scale_length, self.diameters, tuning.frequencies)

    def data_frame(self, scale_length, tuning=GUITAR_STANDARD_TUNING):
        """Return a pandas data frame with all the relevant info.
        """
        tensions = self.tensions(scale_length, tuning)
        data = {'Note': tuning.notes,
                'Diameter [in]': self.diameters,
                'Diameter [mm]': inches_to_mm(self.diameters),
                'Frequency [Hz]': tuning.frequencies,
                'Tension [N]': tensions,
                'Tension [lb]': newton_to_pounds(tensions)
                }
        return pd.DataFrame(data=data)

    def __str__(self):
        """String formatting
        """
        text = f'String gauge {self.name}\n'
        for i, d in enumerate(self.diameters):
            text += f'{i} -> {d:.3f} in ({inches_to_mm(d):.3f} mm)\n'
        return text



class StandardStringGauges:

    EXTRA_SUPER_LIGHT = StringGauge('Extra super light', [.008, .010, .015, .021, .030, .038])
    LIGHT = StringGauge('Light', [.009, .011, .016, .024, .032, .042])
    LIGHT_REGULAR = StringGauge('Light regular', [.009, .011, .016, .026, .036, .046])
    REGULAR = StringGauge('Regular', [.010, .013, .017, .026, .036, .046])
    REGULAR_HEAVY = StringGauge('Regular heavy', [.010, .013, .017, .032, .042, .052])
    MEDIUM = StringGauge('Medium', [.011, .014, .018, .028, .038, .049])
    HEAVY = StringGauge('Heavy', [.012, .016, .024, .032, .042, .052])



if __name__ == '__main__':
    print(newton_to_pounds(string_tension(648., 0.009, 329.63)))
    A = 1.e-12 * STAINLESS_STEEL_DENSITY * numpy.pi * inches_to_mm(1.)**2.
    print(A)
    print(newton_to_pounds(A * (648. * 0.009 * 329.63)**2.))
    print(StandardStringGauges.LIGHT_REGULAR)
    print(StandardStringGauges.LIGHT_REGULAR.tensions(648.))
    print(newton_to_pounds(StandardStringGauges.LIGHT_REGULAR.tensions(648.)))
