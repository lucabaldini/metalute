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

    label : str (optional)
        A text label expressing the intent of the entity
    """

    def __init__(self, name: str = None, label: str = None) -> None:
        """Constructor.
        """
        self.name = name
        self.label = label

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
        if self.label is not None:
            text = '{} [{}]'.format(text, self.label)
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

    label : str (optional)
        A text label expressing the intent of the point
    """

    def __init__(self, x: float = 0., y: float = 0., name: str = None, label: str = None):
        """Constructor.
        """
        self.x = x
        self.y = y
        super().__init__(name, label)

    def __add__(self, other):
        """
        """
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        """
        return self.__class__(self.x - other.x, self.y - other.y)

    def xy(self):
        """
        """
        return (self.x, self.y)

    def text_info(self) -> str:
        """Overloaded method.
        """
        return '({:.2f}, {:.2f})'.format(self.x, self.y)

    def move(self, dist: float, phi: float, name: str = None, label: str = None):
        """
        """
        x = self.x + dist * np.cos(np.radians(phi))
        y = self.y + dist * np.sin(np.radians(phi))
        return Point(x, y, name, label)

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

    def __init__(self, *points, name: str = None, label: str = None):
        """Constructor.
        """
        self.points = points
        super().__init__(name, label)

    def draw(self, offset, **kwargs):
        """
        """
        x = [point.x + offset.x for point in self.points]
        y = [point.y + offset.y for point in self.points]
        line = matplotlib.lines.Line2D(x, y, **kwargs)
        plt.gca().add_line(line)



class CircleArc(GeometricalEntity):

    """
    """

    def __init__(self, center, radius: float, phi1: float = 0., phi2: float = 360.):
        """Constructor.
        """
        self.center = center
        self.radius = radius
        self.phi1 = phi1
        self.phi2 = phi2

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
            p1 = self.center.move(self.radius, self.phi1)
            p2 = self.center.move(self.radius, self.phi2)
            PolyLine(p1, self.center, p2).draw(offset, **fmt)
            d = min(0.80 * self.radius, 10.)
            arc = matplotlib.patches.Arc(xy, d, d, 0., self.phi1, self.phi2, **fmt, **kwargs)
            plt.gca().add_patch(arc)
            self.center.draw(offset, color='lightgrey')
        # And now the actual arc.
        d = 2 * self.radius
        arc = matplotlib.patches.Arc(xy, d, d, 0., self.phi1, self.phi2, **kwargs)
        plt.gca().add_patch(arc)











def line(x, y, **kwargs):
    """
    """
    l = matplotlib.lines.Line2D(x, y, **kwargs)
    plt.gca().add_line(l)


def rectangle(center, width: float, height: float, **kwargs):
    """Draw a rectangle with specified width, height and center.
    """
    kwargs.setdefault('fill', False)
    x, y = center
    x -= width / 2.
    y -= height / 2.
    pos = (x, y)
    patch = matplotlib.patches.Rectangle(pos, width, height, **kwargs)
    plt.gca().add_patch(patch)


def circle(center, radius, **kwargs):
    """Draw a circle.
    """
    kwargs.setdefault('fill', False)
    circle = plt.Circle(center, radius, **kwargs)
    plt.gca().add_patch(circle)


def circle_arc_construction(center, radius: float, phi1: float = 0.,
                            phi2: float = 360., radii: bool = False, **kwargs):
    """Draw all the construction elements for a circle arc.
    """
    kwargs.setdefault('fill', False)
    kwargs.setdefault('color', 'lightgray')
    kwargs.setdefault('ls', 'dashed')
    circle(center, radius, **kwargs)
    if radii:
        kwargs.pop('fill')
        x0, y0 = center
        dx = radius * np.cos(np.radians(phi1))
        dy = radius * np.sin(np.radians(phi1))
        line([x0, x0 + dx], [y0, y0 + dy], **kwargs)
        dx = radius * np.cos(np.radians(phi2))
        dy = radius * np.sin(np.radians(phi2))
        line([x0, x0 + dx], [y0, y0 + dy], **kwargs)


def circle_arc(center, radius: float, phi1: float = 0., phi2: float = 360.,
               construction: bool = False, **kwargs):
    """Draw a circle arc.
    """
    if construction:
        circle_arc_construction(center, radius, phi1, phi2, **kwargs)
    kwargs.setdefault('fill', False)
    d = 2 * radius
    arc = matplotlib.patches.Arc(center, d, d, 0., phi1, phi2, **kwargs)
    plt.gca().add_patch(arc)


def hdim(y, x1, x2, tick=2., va='top', pad=2., label=None, text_size: int = 15):
    """
    """
    if va == 'bottom':
        pad = -pad
    fmt = dict(color='lightgrey')
    plt.hlines(y, x1, x2, **fmt)
    plt.vlines(x1, y - tick, y + tick, **fmt)
    plt.vlines(x2, y - tick, y + tick, **fmt)
    dist = abs(x2 - x1)
    txt = '{:.2f} mm'.format(dist)
    fmt = dict(size=text_size, ha='center', va=va)
    plt.text(0.5 * (x1 + x2), y - pad, txt, **fmt)


def vdim(x, y1, y2, tick=2., ha='left', pad=2., label=None, text_size: int = 15):
    """
    """
    if ha == 'right':
        pad = -pad
    fmt = dict(color='lightgrey')
    plt.vlines(x, y1, y2, **fmt)
    plt.hlines(y1, x - tick, x + tick, **fmt)
    plt.hlines(y2, x - tick, x + tick, **fmt)
    dist = abs(y2 - y1)
    txt = '{:.2f} mm'.format(dist)
    fmt = dict(size=text_size, ha=ha, va='center', rotation=90.)
    plt.text(x + pad, 0.5 * (y1 + y2), txt, **fmt)


def technical_grid(width: float, height: float, margin: float, xdiv: int, ydiv: int,
                   text_size: int = 25):
    """
    """
    l = margin / 2.
    x0 = width / 2. - margin
    y0 = height / 2. - margin
    x = np.linspace(-x0, x0, xdiv + 1)
    y = np.linspace(-y0, y0, ydiv + 1)
    # Draw the small lines on the edges.
    plt.hlines(y, -x0, -x0 - l)
    plt.hlines(y, x0, x0 + l)
    plt.vlines(x, -y0, -y0 - l)
    plt.vlines(x, y0, y0 + l)
    # Draw the letter and numbers.
    dx = x0 / xdiv
    dy = y0 / ydiv
    fmt = dict(size=text_size, ha='center', va='center')
    for i, _x in enumerate(np.flip((x + dx)[:-1])):
        plt.text(_x, -y0 - l, '{}'.format(i + 1), **fmt)
        plt.text(_x, y0 + l, '{}'.format(i + 1), rotation=90., **fmt)
    for i, _y in enumerate((y + dy)[:-1]):
        plt.text(-x0 - l, _y, '{}'.format(ascii_uppercase[i]), **fmt)
        plt.text(x0 + l, _y, '{}'.format(ascii_uppercase[i]), rotation=90., **fmt)


def technical_sheet(figure_name: str, width: float, height: float,
                    margin: float, xdiv: int, ydiv: int, text_size: int = 25):
    """
    """
    plt.figure(figure_name, (mm_to_inches(width), mm_to_inches(height)), 50.)
    plt.gca().set_aspect('equal')
    plt.gca().axis([-width / 2., width / 2., -height / 2., height / 2.])
    plt.subplots_adjust(left=-0.0001, right=1.0001, top=1.0001, bottom=0.)
    w = width - 2. * margin
    h = height - 2. * margin
    rectangle((0., 0.), w, h)
    technical_grid(width, height, margin, xdiv, ydiv, text_size)


def a0sheet(figure_name: str):
    """
    """
    technical_sheet(figure_name, 1189., 841., 30., 16, 12, 25)


def a3sheet(figure_name: str):
    """
    """
    technical_sheet(figure_name, 420., 297., 15., 5, 4, 10)




if __name__ == '__main__':
    from metalute.fret import Fretboard
    a0sheet('Test figure')
    fb = Fretboard()
    fb.draw(position=(200., 0.))
    plt.savefig('fretboard.pdf')
    #plt.show()
