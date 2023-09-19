from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property, dependent_property
from pyuff_ustb.readers import LazyScalar

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class Point(Uff):
    """:class:`Uff` class to define a point location.

    :class:`Point` contains the position of a point in a tridimensional space. It
    express that location in spherical coordinates which allows to place points at
    infinity but in a given direction.

    Original authors:
        Alfonso Rodriguez-Molares (alfonso.r.molares@ntnu.no)
    """

    # Compulsory properties
    @compulsory_property
    def distance(self) -> float:
        "Distance from the point location to the origin of coordinates [m]"
        if "distance" in self._reader:
            return LazyScalar(self._reader["distance"])
        return 0

    @compulsory_property
    def azimuth(self) -> float:
        "Angle from the point location to the plane YZ [rad]"
        if "azimuth" in self._reader:
            return LazyScalar(self._reader["azimuth"])
        return 0

    @compulsory_property
    def elevation(self) -> float:
        "Angle from the point location to the plane XZ [rad]"
        if "elevation" in self._reader:
            return LazyScalar(self._reader["elevation"])
        return 0

    # Dependent properties
    @dependent_property
    def xyz(self) -> np.ndarray:
        "location of the point [m m m] if the point is not at infinity"
        return np.array([self.x, self.y, self.z])

    @dependent_property
    def x(self) -> float:
        return self.distance * np.sin(self.azimuth) * np.cos(self.elevation)

    @dependent_property
    def y(self) -> float:
        return self.distance * np.sin(self.elevation)

    @dependent_property
    def z(self) -> float:
        return self.distance * np.cos(self.azimuth) * np.cos(self.elevation)
