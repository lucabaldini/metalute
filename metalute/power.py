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

"""Power-tools facilities.
"""

from dataclasses import dataclass

import numpy as np

from metalute.blueprint import blueprint
from metalute.geometry2 import Drawable, Point, line, vline, rectangle, circle, hole
from metalute.matplotlib_ import plt



@dataclass
class PowerTool(Drawable):

    """Base class for a power tool.
    """

    brand : str = 'N/A'
    model : str = 'N/A'
    category : str = 'N/A'



@dataclass
class EasyImpact1200(PowerTool):

    """
    """

    brand : str = 'Bosh'
    model : str = 'Easy Impact 1200'
    category : str = 'Drill'



@dataclass
class PST900PEL(PowerTool):

    """
    """

    brand : str = 'Bosh'
    model : str = 'PST 900 PEL'
    category : str = 'Jigsaw'



@dataclass
class POF1400ACE(PowerTool):

    """
    """

    brand : str = 'Bosh'
    model : str = 'POF 1400 ACE'
    category : str = 'Router'
