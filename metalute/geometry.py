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
    """

    def __init__(self, name: str = None) -> None:
        """Constructor.
        """
        self.name = name

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
    """

    def __init__(self, x: float = 0., y: float = 0., name: str = None):
        """Constructor.
        """
        self.x = x
        self.y = y
        super().__init__(name)

    def __add__(self, other):
        """Operator overload.
        """
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Operator overload.
        """
        return self.__class__(self.x - other.x, self.y - other.y)

    def __rmul__(self, const: float):
        """Operator overload.
        """
        return self.__class__(self.x * const, self.y * const)

    def __truediv__(self, const: float):
        """Operator overload.
        """
        return self.__class__(self.x / const, self.y / const)

    def xy(self):
        """Return the two orthogonal coordinates as a 2-element tuple.

        This is handy when we need to pass a Point object to any of the
        matplotlib constructor requiring an (x, y) tuple, such as any of the
        patches classes.
        """
        return (self.x, self.y)

    def distance_to(self, other) -> float:
        """Return the distance to another Point object.
        """
        dx, dy = self - other
        return np.sqrt(dx**2. + dy**2.)

    def text_info(self) -> str:
        """Overloaded method.
        """
        return '({:.2f}, {:.2f})'.format(self.x, self.y)

    def move(self, dist: float, phi: float, name: str = None):
        """Return the point a distance dist from the initial one in a given
        direction.

        Parameters
        ---------
        dist : float
            The distant from the initial point.

        phi : float
            The angle (in degrees) determing the direction to move along,
            measured from the x-axis counter-clockwise.
        """
        x = self.x + dist * np.cos(np.radians(phi))
        y = self.y + dist * np.sin(np.radians(phi))
        return Point(x, y, name)

    def draw(self, offset, ha: str = 'left', va: str = 'bottom', **kwargs):
        """Draw method.
        """
        kwargs.setdefault('color', 'black')
        kwargs.setdefault('markersize', 4.)
        x = self.x + offset.x
        y = self.y + offset.y
        plt.plot(x, y, 'o', **kwargs)
        if self.name is not None:
            kwargs.pop('markersize')
            plt.text(x, y, ' {}'.format(self.name), ha=ha, va=va, **kwargs)



class PolyLine(GeometricalEntity):

    """Class representing a series of straight lines connecting a given set of
    two-dimensional points.
    """

    def __init__(self, *points, name: str = None):
        """Constructor.
        """
        self.points = points
        super().__init__(name)

    def draw(self, offset, **kwargs):
        """Draw method.
        """
        x = [point.x + offset.x for point in self.points]
        y = [point.y + offset.y for point in self.points]
        line = matplotlib.lines.Line2D(x, y, **kwargs)
        plt.gca().add_line(line)



class Line(PolyLine):

    """Class representing a straight line.
    """

    def __init__(self, p1, p2, name: str = None):
        """Constructor.

        Note that we have to pass the name as a keyword argument in order to
        prevent the parent class from swallowing it as an additional point.
        """
        super().__init__(p1, p2, name=name)
        self.p1, self.p2 = self.points

    def length(self):
        """Return the length of the line.
        """
        return self.p1.distance_to(p2)

    def midpoint(self, name: str = None):
        """Return the midpoint of the line.
        """
        p = 0.5 * (self.p1 + self.p2)
        p.name = name
        return p

    def slope(self):
        """Return the slope of the line.
        """
        dx, dy = (self.p2 - self.p1).xy()
        return np.degrees(np.arctan2(dy, dx))



class Circle(GeometricalEntity):

    """Class repesenting a circle.
    """

    def __init__(self, center, radius: float, name: str = None):
        """Constructor.
        """
        super().__init__(name)
        self.center = center
        self.radius = radius

    def diameter(self):
        """Return the diameter of the circle.
        """
        return 2. * self.radius

    def draw(self, offset, **kwargs):
        """Draw method.
        """
        xy = (self.center + offset).xy()
        circle = matplotlib.patches.Circle(xy, self.radius, fill=False, **kwargs)
        plt.gca().add_patch(circle)



class Cross(Circle):

    """Class representing a cross.

    It might look kind of weird to see this as a subclass of Circle, but we are
    taking advantage of the fact that, once we call radius the lenght of the
    arms, the constructors are essentially identical.
    """

    def draw(self, offset, **kwargs):
        """Draw method.
        """
        p0 = self.center.move(self.radius, 180.)
        p1 = self.center.move(self.radius, 0.)
        p2 = self.center.move(self.radius, 90.)
        p3 = self.center.move(self.radius, -90.)
        PolyLine(p0, p1).draw(offset, **kwargs)
        PolyLine(p2, p3).draw(offset, **kwargs)



class Hole(Circle):

    """Class representing a hole.

    And by hole, in this context, we really mean a circle plus a cross,
    specifically for 2-d technical drafting.
    """

    def __init__(self, center, diameter: float, name: str = None):
        """Constructor.
        """
        super().__init__(center, 0.5 * diameter, name)

    def draw(self, offset, **kwargs):
        """Draw method.
        """
        super().draw(offset, **kwargs)
        kwargs.update(color='black')
        Cross(self.center, 1.5 * self.radius).draw(offset, **kwargs)



class CircleArc(Circle):

    """Class representing an arc of a circle.
    """

    def __init__(self, center, radius: float, phi1: float = 0., phi2: float = 360.,
                 name: str = None):
        """Constructor.
        """
        super().__init__(center, radius)
        self.phi1 = phi1
        self.phi2 = phi2

    def start_point(self, name=None):
        """
        """
        return self.center.move(self.radius, self.phi1, name)

    def end_point(self, name=None):
        """
        """
        return self.center.move(self.radius, self.phi2, name)

    def text_info(self) -> str:
        """Overloaded method.
        """
        return '{}, r = {:.2f}, phi = {:.2f}--{:.2f}'.format(self.center, self.radius, self.phi1, self.phi2)

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
                 name: str = None):
        """Constructor.
        """
        super().__init__(name)
        self.center = center
        self.radius = radius
        self.phi1 = phi1
        self.phi2 = phi2

    def point(self, phi, name=None):
        """
        """
        return self.center.move(self.radius(phi), phi, name)

    def start_point(self, name=None):
        """
        """
        return self.point(self.phi1, name)

    def end_point(self, name=None):
        """
        """
        return self.point(self.phi2, name)

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
