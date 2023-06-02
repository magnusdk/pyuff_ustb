from functools import cached_property

import numpy as np

from pyuff.objects import PyuffObject
from pyuff.readers import LazyScalar


class Point(PyuffObject):
    @cached_property
    def distance(self):
        "Distance from the point location to the origin of coordinates [m]"
        return LazyScalar(self._reader["distance"])

    @cached_property
    def azimuth(self):
        "Angle from the point location to the plane YZ [rad]"
        return LazyScalar(self._reader["azimuth"])

    @cached_property
    def elevation(self):
        "Angle from the point location to the plane XZ [rad]"
        return LazyScalar(self._reader["elevation"])

    # Dependent properties
    @property
    def xyz(self):
        "location of the point [m m m] if the point is not at infinity"
        return np.array([self.x, self.y, self.z])

    @property
    def x(self):
        return self.distance * np.sin(self.azimuth) * np.cos(self.elevation)

    @property
    def y(self):
        return self.distance * np.sin(self.elevation)

    @property
    def z(self):
        return self.distance * np.cos(self.azimuth) * np.cos(self.elevation)
