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

"""Docs helper functions.
"""

import os

from metalute import METALUTE_DOCS_TABLES
from metalute.sphinx_ import write_list_table
from metalute.gauge import StandardStringGauges
from metalute.pitch import GUITAR_STANDARD_TUNING
from metalute.units import newton_to_pounds


def write_gauge_tables(scale_length=648.):
    """
    """
    tuning = GUITAR_STANDARD_TUNING
    for gauge in (StandardStringGauges.EXTRA_SUPER_LIGHT,
                  StandardStringGauges.LIGHT,
                  StandardStringGauges.LIGHT_REGULAR,
                  StandardStringGauges.REGULAR,
                  StandardStringGauges.REGULAR_HEAVY,
                  StandardStringGauges.MEDIUM,
                  StandardStringGauges.HEAVY
                  ):
        df = gauge.data_frame(scale_length, tuning)
        file_path = os.path.join(METALUTE_DOCS_TABLES, f'gauge_{gauge.name}.rst')
        file_path = file_path.replace(' ', '_').lower()
        tension = gauge.total_tension(scale_length, tuning)
        caption = f'Summary table for a *{gauge.name}* gauge ({gauge.label()}), '\
                  f'with a standard {tuning} tuning, assuming a {scale_length} mm scale '\
                  f'length (total tension {tension:.2f} N, or {newton_to_pounds(tension):.2f} lb).'
        write_list_table(file_path, df, caption)



def mkaux():
    """
    """
    write_gauge_tables()



if __name__ == '__main__':
    mkaux()
