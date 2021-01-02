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


"""Simple 2-dimensional geometry engine.

This is a complete rewrite of the original attempt, based on the first months
of experience using it for designing things.
"""


from dataclasses import dataclass

import numpy as np
import matplotlib

from metalute.matplotlib_ import plt



@dataclass
class Drawable:

    """Base class for all 2-d drawable objects.
    """

    @staticmethod
    def _parse_offset(offset):
        """Parse the draw offset.
        """
        if isinstance(offset, Point):
            return offset
        if offset is None:
            return Point(0., 0.)
        if isinstance(offset, tuple):
            return Point(*point)
        raise RuntimeError(f'Cannot cast {offset} to Point.')

    def _draw(self, offset, **kwargs):
        """Do nothing _draw method.

        This is intended to be implemented in derived classes.
        """
        raise NotImplementedError

    def draw(self, offset=None, **kwargs):
        """Base draw method.

        This is what gets typically called when we draw stuff, and it is
        accomplishing a few things on top of the actual bare _draw() method, i.e.:

        * it sets the default values for the keyword arguments;
        * it provides a sensible default for the offset parameter;
        * it allows to specify the offset as a 2-element tuple of float, rather
          than a Point instance;
        * it makes sure that the object being draw is returned, so that
          multiple draw operations can be effectively chained.
        """
        kwargs.setdefault('color', 'black')
        offset = self._parse_offset(offset)
        self._draw(offset, **kwargs)
        return self



@dataclass
class Point(Drawable):

    """Point in two dimensions.
    """

    x : float = 0.
    y : float = 0.

    @staticmethod
    def _round(value, digits=3):
        """Small convenience function to round up the coordinates, used below in
        __eq__() and __hash__().

        With three digits we are essentially saying that we consider two points
        to be the same if the difference in both coordinates is smaller than
        1 um.
        """
        return round(10.**digits * value)

    def __eq__(self, other):
        """Operator overload.

        This (along with the fellow __hash__()) is useful if we want remove
        duplicates from a list of points.
        """
        return self._round(self.x) == self._round(other.x) and\
               self._round(self.y) == self._round(other.y)

    def __hash__(self):
        """Operator overload.

        See the comment about __eq__().
        """
        return hash((self._round(self.x), self._round(self.y)))

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

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        kwargs.setdefault('markersize', 4.)
        plt.plot(self.x + offset.x, self.y + offset.y, 'o', **kwargs)

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

    def move(self, dist: float, slope: float):
        """Return the point a distance dist from the initial one in a given
        direction.

        Parameters
        ---------
        dist : float
            The distant from the initial point.

        slope : float
            The angle (in degrees) determing the direction to move along,
            measured from the x-axis counter-clockwise.
        """
        x = self.x + dist * np.cos(np.radians(slope))
        y = self.y + dist * np.sin(np.radians(slope))
        return Point(x, y)

    def hmove(self, dist : float):
        """Move the point horizontally.
        """
        return self.move(dist, 0.)

    def vmove(self, dist : float):
        """Move the point vertically.
        """
        return self.move(dist, 90.)



def point(x : float = 0., y : float = 0., offset=None, **kwargs):
    """Convenience function to draw a point.
    """
    return Point(x, y).draw(offset, **kwargs)



@dataclass
class Line(Drawable):

    """Line in two dimensions.
    """

    start_point : Point
    end_point : Point

    def _draw(self, offset, **kwargs):
        """Overloaded method.

        This could be likely improved, possibly with axline(), that is only
        supported in matplotlib 3.3 and later.
        """
        x1, y1 = (self.start_point + offset).xy()
        x2, y2 = (self.end_point + offset).xy()
        plt.plot((x1, x2), (y1, y2), '-', **kwargs)

    def slope(self):
        """Return the slope of the line.
        """
        dx, dy = (self.end_point - self.start_point).xy()
        return np.degrees(np.arctan2(dy, dx))

    def connecting_line(self, dist : float, slope : float):
        """Return the line departing from the end point of the original one
        with a given slope and length.
        """
        return Line(self.end_point, self.end_point.move(dist, slope))

    def draw_connecting_line(self, length : float, slope : float, offset=None, **kwargs):
        """Draw the connecting line.
        """
        return self.connecting_line(length, slope).draw(offset, **kwargs)

    def connecting_arc(self, radius : float, span_angle : float):
        """Return the circular arc that connects to the end point of the line in
        such a way that the combined path is differentiable all the way through.

        Parameters
        ---------
        radius : float
            The radius of the connecting arc (can be negative).

        span_angle : float
            The measure of the connecting arc.
        """
        slope = self.slope()
        delta = 90. * np.sign(span_angle)
        center = self.end_point.move(radius, slope + delta)
        return Arc(center, radius, slope - delta, span_angle)

    def draw_connecting_arc(self, radius, span_angle, offset=None, **kwargs):
        """Draw a connecting circular arc.
        """
        return self.connecting_arc(radius, span_angle).draw(offset, **kwargs)



def line(start_point, end_point, offset=None, **kwargs):
    """Convenience function to draw a line.
    """
    return Line(start_point, end_point).draw(offset, **kwargs)

def hline(start_point, length, offset=None, **kwargs):
    """Draw a horizontal line.
    """
    return Line(start_point, start_point.vmove(length)).draw(offset, **kwargs)

def vline(start_point, length, offset=None, **kwargs):
    """Draw a vertical line.
    """
    return Line(start_point, start_point.hmove(length)).draw(offset, **kwargs)



@dataclass
class Rectangle(Drawable):

    """A rectangle.
    """

    center : Point
    width : float
    height : float
    corner_radius : float = 0.

    def __post_init__(self):
        """Overloaded method.
        """
        assert self.width >= 0.
        assert self.height >= 0.
        assert self.corner_radius >= 0.

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        p = self.center + Point(-0.5 * self.width, -0.5 * self.height) + offset
        p = p.vmove(self.corner_radius)
        w = self.width - 2. * self.corner_radius
        h = self.height - 2. * self.corner_radius
        r = self.corner_radius
        line(p, p.vmove(h)).draw_connecting_arc(r, -90.).draw_connecting_line(w).\
            draw_connecting_arc(r, -90.).draw_connecting_line(h).\
            draw_connecting_arc(r, -90.).draw_connecting_line(w).\
            draw_connecting_arc(r, -90.)



def rectangle(center, width, height, corner_radius=0., offset=None, **kwargs):
    """Draw a rectangle.
    """
    return Rectangle(center, width, height, corner_radius).draw(offset, **kwargs)



@dataclass
class Cap(Drawable):

    """
    """

    start_point : float
    start_slope : float
    base : float
    height : float
    corner_radius : float = 0.

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        b = self.base - 2. * self.corner_radius
        h = self.height - self.corner_radius
        line(self.start_point, self.start_point.move(h, self.start_slope), offset).\
            draw_connecting_arc(self.corner_radius, 90., offset).\
            draw_connecting_line(b, offset).\
            draw_connecting_arc(self.corner_radius, 90., offset).\
            draw_connecting_line(h, offset)



def cap(start_point, start_slope, base, height, corner_radius=0., offset=None, **kwargs):
    """Draw a Cap.
    """
    return Cap(start_point, start_slope, base, height, corner_radius).draw(offset, **kwargs)

def ccap(start_point, base, height, corner_radius=0., offset=None, **kwargs):
    """Draw a c-like Cap.
    """
    return Cap(start_point, 180., base, height, corner_radius).draw(offset, **kwargs)

def rccap(start_point, base, height, corner_radius=0., offset=None, **kwargs):
    """Draw a reverse c-like Cap.
    """
    return Cap(start_point, 0., base, height, corner_radius).draw(offset, **kwargs)

def ucap(start_point, base, height, corner_radius=0., offset=None, **kwargs):
    """Draw a u-like Cap.
    """
    return Cap(start_point, -90., base, height, corner_radius).draw(offset, **kwargs)

def rucap(start_point, base, height, corner_radius=0., offset=None, **kwargs):
    """Draw a reverse u-like Cap.
    """
    return Cap(start_point, 90., base, height, corner_radius).draw(offset, **kwargs)




@dataclass
class Arc(Drawable):

    """Class representing a circular arc.

    Although this is using the matplotlib.patches.Arc class under the hood, the
    interface in the constructor is deliberately different, as we use the
    orientation of the initial point (start_angle) and the span (span_angle),
    rather than the initial and the final angles (theta1 and theta2).
    This is more germane to the way we usually define arcs, i.e., by the
    starting point and the span.

    Also, in matplotlib the arc is always drawn in the counterclockwise
    direction, while here we always keep track of the start point and the end
    point, and we control the direction by allowing the arc measure to be
    negative.
    """

    center : Point
    radius : float
    start_angle : float = 0.
    span_angle : float = 360.

    def __post_init__(self):
        """
        """
        assert self.radius >= 0.

    def start_point(self):
        """Return the start point of the arc.
        """
        return self.center.move(self.radius, self.start_angle)

    def end_point(self):
        """Return the end point of the arc.
        """
        return self.center.move(self.radius, self.end_angle())

    def end_angle(self):
        """Return the end angle of the arc.
        """
        return self.start_angle + self.span_angle

    def end_slope(self):
        """Return the slope of the line that connects to the end point of the
        arc in such a way that the combined path is differentiable all the way
        through.
        """
        return self.end_angle() + 90. + 180. * (self.span_angle < 0.)

    def _draw(self, offset, **kwargs):
        """Draw the circular arc.
        """
        xy = (self.center + offset).xy()
        d = 2. * self.radius
        # Mind that matplotlib is always drawing arcs counterclockwise, so we
        # do have to swap the extremes if the arc measure is negative.
        theta1 = self.start_angle
        theta2 = self.end_angle()
        if self.span_angle < 0.:
            theta1, theta2 = theta2, theta1
        _arc = matplotlib.patches.Arc(xy, d, d, 0., theta1, theta2, **kwargs)
        plt.gca().add_patch(_arc)
        return self

    def connecting_line(self, dist : float):
        """Return the line departing from the end point of the arc
        """
        p = self.end_point()
        return Line(p, p.move(dist, self.end_slope()))

    def draw_connecting_line(self, length : float, offset=None, **kwargs):
        """Draw the connecting line.
        """
        return self.connecting_line(length).draw(offset, **kwargs)



def arc(center, radius, start_angle=0., span_angle=360., offset=None, **kwargs):
    """Draw a circular arc.
    """
    return Arc(center, radius, start_angle, span_angle).draw(offset, **kwargs)



@dataclass
class Cross(Drawable):

    """A cross.
    """

    center : Point
    radius : float

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        p0 = self.center + offset
        line(p0.hmove(-self.radius), p0.hmove(self.radius))
        line(p0.vmove(-self.radius), p0.vmove(self.radius))



def cross(center, radius, offset=None, **kwargs):
    """Drwa a cross.
    """
    return Cross(center, radius).draw(offset, **kwargs)



@dataclass
class Circle(Drawable):

    """A plain circle.
    """

    center : Point
    radius : float

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        xy = (self.center + offset).xy()
        d = 2. * self.radius
        _arc = matplotlib.patches.Arc(xy, d, d, 0., 0., 360., **kwargs)
        plt.gca().add_patch(_arc)
        return self



def circle(center, radius, offset=None, **kwargs):
    """Draw a circle.
    """
    return Arc(center, radius).draw(offset, **kwargs)



@dataclass
class Hole(Drawable):

    """A hole, i.e., a circle with a cross.
    """

    center : Point
    diameter : float
    cross_scale : float = 1.25

    def __post_init__(self):
        """
        """
        assert self.diameter >= 0
        self.radius = 0.5 * self.diameter

    def _draw(self, offset, **kwargs):
        """Overloaded method.
        """
        circle(self.center, self.radius, offset, **kwargs)
        cross(self.center, self.radius * self.cross_scale, offset, **kwargs)



def hole(center, diameter, cross_scale=1.25, offset=None, **kwargs):
    """Draw a hole.
    """
    return Hole(center, diameter, cross_scale).draw(offset, **kwargs)
