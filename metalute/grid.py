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

"""Measuring grid.
"""

import numpy as np

from metalute.geometry import a3sheet, plt, circle, hdim, vdim, line


nx = 16
ny = 10
mx = 6
my = 4
pitch = 10.
r1 = 0.2 * pitch
r2 = 0.8 * pitch
w = 50.

a3sheet('A3 grid')

for i in range(-nx, nx + 1):
    for j in range(-ny, ny + 1):
        if abs(i) >= mx or abs(j) >= my:
            circle((i * pitch, j * pitch), r1, fill=True, facecolor='black')

x = (nx + 1) * pitch
y = (ny + 1) * pitch
circle((x, y), r2, fill=True, facecolor='black')
circle((-x, y), r2, fill=True, facecolor='black')
circle((x, -y), r2, fill=True, facecolor='black')
circle((-x, -y), r2, fill=True, facecolor='black')

fmt = dict(text_size=10)
hdim(y + 1.5 * pitch, -x, x, **fmt)
hdim(-y - 1.5 * pitch, -x, 0, va='bottom', **fmt)
vdim(x + 1.5 * pitch, -y, y, ha='right', **fmt)
vdim(-x - 1.5 * pitch, -y, 0, **fmt)

plt.hlines(0., -w, w)
x = np.arange(-w, 1.01 * w, 10.)
y = 2.5
plt.vlines(x, 0., y)
for i, _x in enumerate(x):
    plt.text(_x, y, '{}'.format(i), va='bottom', ha='center', size=10)

plt.savefig('a3_grid.pdf')

plt.show()
