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
    properties (e.g., the name) that are common to all such entities.

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

    @classmethod
    def __roundup(cls, val, digits=3):
        """Small convenience function to round up the coordinates, used below in
        __eq__() and __hash__().

        With three digits we are essentially saying that we consider two points
        to be the same if the difference in both coordinates is smaller than
        1 um.
        """
        return round(10**digits * val)

    def __eq__(self, other):
        """Operator overload.

        This (along with the fellow __hash__()) is useful if we want remove
        duplicates from a list of points.
        """
        return self.__roundup(self.x) == self.__roundup(other.x) and\
               self.__roundup(self.y) == self.__roundup(other.y)

    def __hash__(self):
        """Operator overload.

        See the comment about __eq__().
        """
        return hash((self.__roundup(self.x), self.__roundup(self.y)))

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


class Path(GeometricalEntity):

    """Do nothing GeometricalEntity subclass.

    This is esentially to distinguish points from paths with the possible
    geometrical entities.
    """

    def draw_construction(self, offset, **kwargs):
        """Do-nothing method to provide a unified interface for drawing
        intermediate steps of path construction.

        Subclasses can re-implement this in odrer to do something useful.
        """
        pass

    def reference_points(self):
        """Do-nothing hook to return a set of refernce points for the shape.

        In the default implementation this is returning an empty list.
        """
        return []



class PolyLine(Path):

    """Class representing a series of straight lines connecting a given set of
    two-dimensional points.
    """

    def __init__(self, *points, name: str = None):
        """Constructor.
        """
        self.points = points
        super().__init__(name)

    def reference_points(self):
        """Overloaded method.
        """
        return self.points

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

    def __init__(self, start_point, end_point, name: str = None):
        """Constructor.

        Note that we have to pass the name as a keyword argument in order to
        prevent the parent class from swallowing it as an additional point.
        """
        super().__init__(start_point, end_point, name=name)
        self.start_point, self.end_point = self.points

    @classmethod
    def from_start_point_and_dir(cls, start_point, length, slope, name):
        """Different constructor.
        """
        end_point = start_point.move(length, slope)
        return cls(start_point, end_point, name)

    def length(self):
        """Return the length of the line.
        """
        return self.start_point.distance_to(self.end_point)

    def midpoint(self, name: str = None):
        """Return the midpoint of the line.
        """
        p = 0.5 * (self.start_point + self.end_point)
        p.name = name
        return p

    def slope(self):
        """Return the slope of the line.
        """
        dx, dy = (self.end_point - self.start_point).xy()
        return np.degrees(np.arctan2(dy, dx))

    def text_info(self) -> str:
        """Overloaded method.
        """
        return '{}--{}'.format(self.start_point, self.end_point)



class Circle(Path):

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



class CircularArc(Circle):

    """Class representing a circular arc.

    Although this is using the matplotlib.patches.Arc class under the hood, the
    interface in the constructor is deliberately different, as we use the
    orientation of the initial point (start_phi) and the span (delta_phi),
    rather than the initial and the final angles (theta1 and theta2).
    This is more germane to the way we usually define arcs, i.e., by the
    starting point and the span.

    Also, in matplotlib the arc is always drawn in the counterclockwise
    direction, while here we always keep track of the start point and the end
    point, and we control the direction by allowing the arc measure to be
    negative.

    Parameters
    ---------
    center : Point instance
        The center of the circular arc.

    radius : float
        The radius of the circular arc

    start_phi : float, in [0., 360.]
        The angle (in degrees) subtended by the starting point of the arc.

    span : float, in [-360, 360]
        The arc measure in degrees.

    name : string (optional)
        The name of the arc.
    """

    def __init__(self, center, radius: float, start_phi: float = 0.,
                 span: float = 360., name: str = None):
        """Constructor.
        """
        super().__init__(center, radius, name)
        self.start_phi = start_phi
        self.span = span

    @property
    def end_phi(self):
        """Return the angle of the end point with respect to the center.
        """
        return self.start_phi + self.span

    def orientation(self):
        """Return 1. if the arc is rotating counter-clockwise and -1. vice versa.
        """
        return np.sign(self.span)

    def length(self):
        """Return the length of the arc.
        """
        return 2. * np.pi * self.radius * self.span / 360.

    def start_point(self, name=None):
        """Return the start point of the arc.
        """
        return self.center.move(self.radius, self.start_phi, name)

    def end_point(self, name=None):
        """Return the end point of the arc.
        """
        return self.center.move(self.radius, self.end_phi, name)

    def reference_points(self):
        """Overloaded method.
        """
        return [self.start_point(), self.end_point()]

    def start_slope(self):
        """Not implemented, yet.

        We might want to implement this functionality of we ever need to connect
        more paths at the start of arc, rather than at the end (which is by far
        the most common case).
        """
        raise NotImplementedError

    def end_slope(self):
        """Return the slope of the line that connects to the end point of the
        arc in such a way that the combined path is differentiable all the way
        through.
        """
        return self.end_phi + 90. * self.orientation()

    def connecting_line(self, length, name=None):
        """Return the line that connects to the end point of the arc in such a
        way that the combined path is differentiable all the way through.
        """
        start_point = self.end_point()
        end_point = start_point.move(length, self.end_slope())
        return Line(start_point, end_point, name)

    def connecting_circular_arc(self, radius, span, name=None):
        """Return the circular arc that connects to the end point of the arc in
        such a way that the combined path is differentiable all the way through.

        Parameters
        ---------
        radius : float
            The radius of the connecting arc. If the radius is negative the
            connecting arc is intended as the one with the opposite curvature
            of the original.

        span : float
            The measure of the connecting arc.
        """
        slope = self.end_phi
        if radius > 0:
            slope += 180.
        radius = abs(radius)
        center = self.end_point().move(radius, slope)
        return CircularArc(center, radius, self.end_phi, span * self.orientation())

    def text_info(self) -> str:
        """Overloaded method.
        """
        args = self.center, self.radius, self.start_phi, self.span
        return '{}, r = {:.2f}, phi = {:.2f} -> {:.2f}'.format(*args)

    def draw_construction(self, offset, **kwargs):
        """Draw the geometrical construction of the circular arc.

        Note that this should always be called before the draw() method, so that
        all the paths get overlaid in the right order.
        """
        xy = (self.center + offset).xy()
        kwargs.setdefault('color', 'lightgrey')
        self.center.draw(offset, **kwargs)
        kwargs.setdefault('ls', 'dashed')
        Circle(self.center, self.radius).draw(offset, **kwargs)
        PolyLine(self.start_point(), self.center, self.end_point()).draw(offset, **kwargs)
        # This should definitely be improved.
        r = min(0.35 * self.radius, 8.)
        CircularArc(self.center, r, self.start_phi, self.span).draw(offset, **kwargs)

    def draw(self, offset, **kwargs):
        """Draw the circular arc.
        """
        xy = (self.center + offset).xy()
        d = self.diameter()
        theta1 = self.start_phi
        theta2 = self.end_phi
        # Mind that matplotlib is always drawing arcs counterclockwise, so we
        # do have to swap the extremes if the arc measure is negative.
        if self.span < 0.:
            theta1, theta2 = theta2, theta1
        arc = matplotlib.patches.Arc(xy, d, d, 0., theta1, theta2, **kwargs)
        plt.gca().add_patch(arc)



class ParametricPolyPathBase(Path):

    """Class describing a parametric curve constructed as a series of connecting
    path elements.

    This is an admittedly complicated object, that is meant to creat complex
    shapes (e.g., guitar bodies or headstocks) combining simpler paths, such as
    lines or arcs.

    At the fundamental level, a ParametricPolyPath encapsulates two
    dictionaries, the first one holding all the parameter values, and the second
    containing all the path objects composing the complex shape. The basic rules
    are:

    * all the keyword arguments passed to the constructor update the default
    parameter values;
    * the class is designed in such a way that cannot be directly instantiated,
    and *has to be subclassed*, instead; all subclasses should overload the
    construct() method to build the actual complex path;
    * the construct() method should always return the return value of a locals()
    call;
    * the constructor of the base class picks up the return value of construct()
    and collects all the Path objects in there, populating the corresponding
    dictionary; from this point on, the complex path is ready to be used
    (e.g., you can draw it).
    """

    DEFAULT_PAR_DICT = {}

    def __init__(self, **kwargs):
        """At the construction stage the default parameters are updated
        based on whatever is passed as an argument.

        Mind the first line is a shallow copy, so care should be taken if any
        of the parameter is mutable (but we should typically stick to simple
        things, like numbers or booleans).
        """
        self.par_dict = self.DEFAULT_PAR_DICT.copy()
        self.par_dict.update(**kwargs)
        self.anchor = Point(0., 0., 'anchor')
        self.path_dict = {}
        self.__finalize(self.construct())

    def __getattr__(self, name):
        """Overloaded method so that the parameters can be accessed by name
        within the class.
        """
        return self.par_dict[name]

    def construct(self):
        """No-op method to be overloaded by derived classes.

        This is where all the dirty work should happen.
        """
        raise NotImplementedError

    def add_path(self, path):
        """Add a path to the complex shape.

        Note that all the Path objects are indexed by name in the dictionary.
        """
        self.path_dict[path.name] = path

    def __finalize(self, locals_):
        """Collect all the Path objects returned by construct() and put them
        into the proper dictionary.

        Note that self is returned by the locals() call in the subclass, so that
        we need to add an explicit check, here, in order to avoid infinite
        recursion.
        """
        for name, obj in locals_.items():
            if isinstance(obj, Path) and not isinstance(obj, self.__class__):
                obj.name = name
                self.add_path(obj)

    def draw_reference_points(self, offset, **kwargs):
        """Draw the reference points for all the sub-paths.
        """
        points = []
        for path in self.path_dict.values():
            for p in path.reference_points():
                if p not in points:
                    points.append(p)
        for i, p in enumerate(points):
            # Mind we create a copy of the original point so that we can
            # set the name according to the index without modifying the
            # original.
            Point(p.x, p.y, '{:d}'.format(i + 1)).draw(offset, **kwargs)

    def draw_construction(self, offset, **kwargs):
        """Draw the object.
        """
        for path in self.path_dict.values():
            path.draw_construction(offset, **kwargs)

    def draw(self, offset, **kwargs):
        """Draw the object.
        """
        for path in self.path_dict.values():
            path.draw(offset, **kwargs)







"""Following to be deprecated.
"""
class SpiralArc(Path):

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
