import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property, dependent_property
from pyuff_ustb.readers import LazyScalar


class Point(Uff):
    # Compulsory properties
    @compulsory_property
    def distance(self) -> float:
        "Distance from the point location to the origin of coordinates [m]"
        return LazyScalar(self._reader["distance"])

    @compulsory_property
    def azimuth(self) -> float:
        "Angle from the point location to the plane YZ [rad]"
        return LazyScalar(self._reader["azimuth"])

    @compulsory_property
    def elevation(self) -> float:
        "Angle from the point location to the plane XZ [rad]"
        return LazyScalar(self._reader["elevation"])

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
