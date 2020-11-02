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
import sys

from metalute import METALUTE_DOCS_TABLES, METALUTE_DOCS
from metalute.sphinx_ import write_list_table
from metalute.gauge import StandardStringGauges
from metalute.pitch import GUITAR_STANDARD_TUNING
from metalute.units import newton_to_pounds
from metalute.head import MusicMan
from metalute.body import MusicManAxis
from metalute.geometry import Point
#from metalute.blueprint import blueprint
from metalute.matplotlib_ import plt, setup_page

if sys.flags.interactive:
    plt.ion()


def write_gauge_tables(scale_length=648.):
    """Write the summary tables for the different string gauges.
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


def write_logo(width=450., height=350, dpi=100, text_size=3., line_width=2.5, margin=-0.01):
    """Create the logo for the package.
    """
    body = MusicManAxis()
    offset = Point(-200., 0.)
    width, height, dpi = setup_page((width, height), dpi, text_size, line_width)
    plt.figure('metalute logo')
    plt.gca().set_aspect('equal')
    hmargin = margin
    vmargin = hmargin * width / height
    plt.subplots_adjust(left=hmargin, right=1. - hmargin, top=1. - vmargin, bottom=vmargin)
    plt.xticks([])
    plt.yticks([])
    w = 0.5 * width * (1. - 2. * hmargin)
    h = 0.5 * height * (1. - 2. * vmargin)
    plt.gca().axis([-w, w, -h, h])
    body.draw(offset)
    kwargs = dict(ha='center', va='center', family='DejaVu Sans Mono')
    plt.text(-75., 40., 'M', **kwargs, size=450)
    plt.text(20., 18., 'eta', **kwargs, size=150, color='orange')
    plt.text(-51., -50., 'L', **kwargs, size=450)
    plt.text(-8., -55., 'ute', **kwargs, size=150, color='orange')
    plt.tight_layout(pad=-1.)
    file_path = os.path.join(METALUTE_DOCS, '_static', 'metalute_logo.png')
    plt.savefig(file_path)


def mkaux():
    """
    """
    #write_gauge_tables()
    write_logo()



if __name__ == '__main__':
    mkaux()
