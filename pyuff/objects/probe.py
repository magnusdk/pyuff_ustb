from functools import cached_property

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray
import numpy as np


class Probe(PyuffObject):
    @cached_property
    def geometry(self):
        """An array with attitude of rectangular elements.

        The array contains 7 fields (over all elements):
        [
            x,      # [m]
            y,      # [m]
            z,      # [m]
            theta,  # [rad]
            phi,    # [rad]
            width,  # [m]
            height, # [m]
        ]

        The shape of the returned array is (7, n_elements)."""
        return LazyArray(self._reader["geometry"])

    @cached_property
    def origin(self):
        "Location of the probe respect to origin of coordinates"
        from pyuff.objects.point import Point

        if "origin" in self._reader:
            return Point(self._reader["origin"])

    # Dependent properties
    @property
    def n_elements(self):
        "Number of elements"
        return self.geometry.shape[1]

    @property
    def x(self):
        "Center of the element in the x axis [m]"
        return self.geometry[0]

    @property
    def y(self):
        "Center of the element in the y axis [m]"
        return self.geometry[1]

    @property
    def z(self):
        "Center of the element in the z axis [m]"
        return self.geometry[2]

    @property
    def xyz(self):
        "Center of the element as an array of shape (n_elements, 3) [m]"
        return np.stack([self.x, self.y, self.z], 1)

    @property
    def theta(self):
        "Orientation of the element in the azimuth direction [rad]"
        return self.geometry[3]

    @property
    def phi(self):
        "Orientation of the element in the elevation direction [rad]"
        return self.geometry[4]

    @property
    def width(self):
        "Element width [m]"
        return self.geometry[5]

    @property
    def height(self):
        "Element height [m]"
        return self.geometry[6]

    @property
    def r(self):
        "Distance from the element center to the origin of coordinates [m]"
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
