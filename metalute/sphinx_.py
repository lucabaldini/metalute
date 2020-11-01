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

"""Sphinx helper function.
"""

import pandas as pd


def write_list_table(file_path : str, data : dict, caption='', **kwargs):
    """
    """
    if isinstance(data, pd.DataFrame):
        data = data.to_dict(orient='list')
    with open(file_path, 'w') as output_file:
        output_file.write(f'.. list-table:: {caption}\n')
        for key, value in kwargs:
            output_file.write(f'   :{key}: {value}\n')
        output_file.write('\n')
        for i, key in enumerate(data.keys()):
            if i == 0:
                output_file.write(f'   * - {key}\n')
            else:
                output_file.write(f'     - {key}\n')
        for row in zip(*data.values()):
            for i, val in enumerate(row):
                if i == 0:
                    output_file.write(f'   * - {val}\n')
                else:
                    output_file.write(f'     - {val:.3f}\n')
