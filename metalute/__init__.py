# -*- coding: utf-8 -*-
#
# Copyright (C) 2019--2020 Luca Baldini (luca.baldini@pi.infn.it)
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


"""Definition of the underlying environment for the package and related
utility functions.
"""

import os
import logging


# Basic local environment.
#
BASE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def _join(*args) -> str:
    """Path concatenation relatove to the bas package folder (avoids some typing.)
    """
    return os.path.join(BASE_FOLDER, *args)


GITHUB_URL = 'https://github.com/lucabaldini/metalute'
ROOT_FOLDER = _join('metalute')
TEST_FOLDER = _join('tests')
TEST_DATA_FOLDER = os.path.join(TEST_FOLDER, 'data')
METALUTE_DOCS = _join('docs')
METALUTE_DOCS_FIGURES = os.path.join(METALUTE_DOCS, 'figures')
METALUTE_DOCS_TABLES = os.path.join(METALUTE_DOCS, 'tables')
