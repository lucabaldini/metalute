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

"""Geometry-related facilities.
"""

from string import ascii_uppercase

import numpy as np

from metalute.matplotlib_ import matplotlib, plt
from metalute.units import mm_to_inches


class GeometricalEntity:

    """Base class for concrete geometrical entities.

    This is a base class from which all geometrical entities defined in this
    module (such as points, lines and shapes) inherit from. It encapsulates the
    properties (e.g., name and label) that are common to all such entities.

    Parameters
    ---------
    name : str (optional)
        The unique name of the entity

    intent : str (optional)
        A text label expressing the intent of the entity
    """

    def __init__(self, name: str = None, intent: str = None) -> None:
        """Constructor.
        """
        self.name = name
        self.intent = intent

    def text_info(self) -> str:
        """Basic textual information for the entity.

        This is intended to be derived by the subclasses to provide specific
        information (e.g., the coordinates of a given point) and is used by the
        __str__ dunder method defined in this base class.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """String formatting.
        """
        text = self.name or self.__class__.__name__
        text = '{}: {}'.format(text, self.text_info())
        if self.intent is not None:
            text = '{} [{}]'.format(text, self.intent)
        return text



class Point(GeometricalEntity):

    """Small utility class representing a point in two dimensions.

    Parameters
    ---------
    x : float
        The x coordinate of the point

    y : float
        The y coordinate of the point

    name : str (optional)
        The unique name of the point

    intent : str (optional)
        A text label expressing the intent of the point
    """

    def __init__(self, x: float = 0., y: float = 0., name: str = None, intent: str = None):
        """Constructor.
        """
        self.x = x
        self.y = y
        super().__init__(name, intent)

    def __add__(self, other):
        """
        """
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        """
        return self.__class__(self.x - other.x, self.y - other.y)

    def __rmul__(self, const: float):
        """
        """
        return self.__class__(self.x * const, self.y * const)

    def __truediv__(self, const: float):
        """
        """
        return self.__class__(self.x / const, self.y / const)

    def xy(self):
        """
        """
        return (self.x, self.y)

    def distance_to(self, other):
        """
        """
        dx, dy = self - other
        return np.sqrt(dx**2. + dy**2.)

    def text_info(self) -> str:
        """Overloaded method.
        """
        return '({:.2f}, {:.2f})'.format(self.x, self.y)

    def move(self, dist: float, phi: float, name: str = None, intent: str = None):
        """
        """
        x = self.x + dist * np.cos(np.radians(phi))
        y = self.y + dist * np.sin(np.radians(phi))
        return Point(x, y, name, intent)

    def draw(self, offset, name: bool = True, ha: str = 'left', va: str = 'bottom', **kwargs):
        """Draw the point.
        """
        kwargs.setdefault('color', 'black')
        kwargs.setdefault('markersize', 4.)
        x = self.x + offset.x
        y = self.y + offset.y
        plt.plot(x, y, 'o', **kwargs)
        if name and (self.name is not None):
            kwargs.pop('markersize')
            plt.text(x, y, ' {}'.format(self.name), ha=ha, va=va, **kwargs)



class PolyLine(GeometricalEntity):

    """
    """

    def __init__(self, *points, name: str = None, intent: str = None):
        """Constructor.
        """
        self.points = points
        super().__init__(name, intent)

    def draw(self, offset, **kwargs):
        """
        """
        x = [point.x + offset.x for point in self.points]
        y = [point.y + offset.y for point in self.points]
        line = matplotlib.lines.Line2D(x, y, **kwargs)
        plt.gca().add_line(line)



class Line(PolyLine):

    """
    """

    def __init__(self, p1, p2, name: str = None, intent: str = None):
        """Constructor.
        """
        super().__init__(p1, p2, name=name, intent=intent)
        self.p1, self.p2 = self.points

    def length(self):
        """
        """
        dx, dy = (self.p2 - self.p1).xy()
        return np.sqrt(dx ** 2. + dy **2.)

    def midpoint(self):
        """
        """
        return 0.5 * (self.p1 + self.p2)

    def slope(self):
        """
        """
        dx, dy = (self.p2 - self.p1).xy()
        return np.degrees(np.arctan2(dy, dx))



class Circle(GeometricalEntity):

    """
    """

    def __init__(self, center, radius: float, name: str = None, intent: str = None):
        """Constructor.
        """
        super().__init__(name, intent)
        self.center = center
        self.radius = radius

    def diameter(self):
        """
        """
        return 2. * self.radius

    def draw(self, offset, **kwargs):
        """
        """
        xy = (self.center + offset).xy()
        circle = matplotlib.patches.Circle(xy, self.radius, fill=False, **kwargs)
        plt.gca().add_patch(circle)



class Cross(Circle):

    """
    """

    def draw(self, offset, **kwargs):
        """
        """
        p0 = self.center.move(self.radius, 180.)
        p1 = self.center.move(self.radius, 0.)
        p2 = self.center.move(self.radius, 90.)
        p3 = self.center.move(self.radius, -90.)
        PolyLine(p0, p1).draw(offset, **kwargs)
        PolyLine(p2, p3).draw(offset, **kwargs)



class Hole(Circle):

    """
    """

    def __init__(self, center, diameter: float, name: str = None, intent: str = None):
        """
        """
        super().__init__(center, 0.5 * diameter, name, intent)

    def draw(self, offset, **kwargs):
        """
        """
        super().draw(offset, **kwargs)
        kwargs.update(color='black')
        Cross(self.center, 1.5 * self.radius).draw(offset, **kwargs)



class CircleArc(Circle):

    """
    """

    def __init__(self, center, radius: float, phi1: float = 0., phi2: float = 360.,
                 name: str = None, intent: str = None):
        """Constructor.
        """
        super().__init__(center, radius, name, intent)
        self.phi1 = phi1
        self.phi2 = phi2

    def start_point(self, name=None, intent=None):
        """
        """
        return self.center.move(self.radius, self.phi1, name, intent)

    def end_point(self, name=None, intent=None):
        """
        """
        return self.center.move(self.radius, self.phi2, name, intent)

    def draw(self, offset, full_circle: bool = True, radii: bool = True, **kwargs):
        """
        """
        xy = (self.center + offset).xy()
        # This needs to go first, as the construction is in background.
        if full_circle:
            fmt = dict(ls='dashed', fill=False, color='lightgrey')
            circle = plt.Circle(xy, self.radius, **fmt, **kwargs)
            plt.gca().add_patch(circle)
        if radii:
            fmt = dict(ls='dashed', color='lightgrey')
            p1 = self.start_point()
            p2 = self.end_point()
            PolyLine(p1, self.center, p2).draw(offset, **fmt)
            d = min(0.80 * self.radius, 10.)
            arc = matplotlib.patches.Arc(xy, d, d, 0., self.phi1, self.phi2, **fmt, **kwargs)
            plt.gca().add_patch(arc)
            self.center.draw(offset, color='lightgrey')
        # And now the actual arc.
        d = 2 * self.radius
        arc = matplotlib.patches.Arc(xy, d, d, 0., self.phi1, self.phi2, **kwargs)
        plt.gca().add_patch(arc)



class SpiralArc(GeometricalEntity):

    """Class describing a spiral arc.
    """

    def __init__(self, center, radius, phi1: float = 0., phi2: float = 360.,
                 name: str = None, intent: str = None):
        """Constructor.
        """
        super().__init__(name, intent)
        self.center = center
        self.radius = radius
        self.phi1 = phi1
        self.phi2 = phi2

    def point(self, phi, name=None, intent=None):
        """
        """
        return self.center.move(self.radius(phi), phi, name, intent)

    def start_point(self, name=None, intent=None):
        """
        """
        return self.point(self.phi1)

    def end_point(self, name=None, intent=None):
        """
        """
        return self.point(self.phi2)

    def slope_at_start_point(self):
        """
        """
        return Line(self.point(self.phi1), self.point(self.phi1 - 0.1)).slope()

    def slope_at_end_point(self):
        """
        """
        pass

    def draw(self, offset, num_points: int = 250, construction: bool = True, **kwargs):
        """
        """
        kwargs.setdefault('color', 'black')
        x0, y0 = (self.center + offset).xy()
        phi = np.linspace(self.phi1, self.phi2, num_points)
        r = self.radius(phi)
        x = x0 + r * np.cos(np.radians(phi))
        y = y0 + r * np.sin(np.radians(phi))
        # This needs to go first, as the construction is in background.
        if construction:
            fmt = dict(ls='dashed', color='lightgrey')
            p1 = self.start_point()
            p2 = self.end_point()
            PolyLine(p1, self.center, p2).draw(offset, **fmt)
            d = 10.
            arc = matplotlib.patches.Arc((x0, y0), d, d, 0., self.phi1, self.phi2, **fmt)
            plt.gca().add_patch(arc)
            self.center.draw(offset, color='lightgrey')
        plt.plot(x, y, **kwargs)
