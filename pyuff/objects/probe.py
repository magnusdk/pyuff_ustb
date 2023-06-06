import numpy as np

from pyuff.objects.base import PyuffObject, compulsory_property, dependent_property
from pyuff.readers import LazyArray


class Probe(PyuffObject):
    # Compulsory properties
    @compulsory_property
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

    @compulsory_property
    def origin(self):
        "Location of the probe respect to origin of coordinates"
        from pyuff.objects.point import Point

        if "origin" in self._reader:
            return Point(self._reader["origin"])

    # Dependent properties
    @dependent_property
    def n_elements(self):
        "Number of elements"
        return self.geometry.shape[1]

    @dependent_property
    def x(self):
        "Center of the element in the x axis [m]"
        return self.geometry[0]

    @dependent_property
    def y(self):
        "Center of the element in the y axis [m]"
        return self.geometry[1]

    @dependent_property
    def z(self):
        "Center of the element in the z axis [m]"
        return self.geometry[2]

    @dependent_property
    def xyz(self):
        "Center of the element as an array of shape (n_elements, 3) [m]"
        return np.stack([self.x, self.y, self.z], -1)

    @dependent_property
    def theta(self):
        "Orientation of the element in the azimuth direction [rad]"
        return self.geometry[3]

    @dependent_property
    def phi(self):
        "Orientation of the element in the elevation direction [rad]"
        return self.geometry[4]

    @dependent_property
    def width(self):
        "Element width [m]"
        return self.geometry[5]

    @dependent_property
    def height(self):
        "Element height [m]"
        return self.geometry[6]

    @dependent_property
    def r(self):
        "Distance from the element center to the origin of coordinates [m]"
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
