from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property, dependent_property
from pyuff_ustb.readers import LazyArray, LazyScalar

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class Phantom(Uff):
    """:class:`Uff` class for a phantom definition.

    Original authors:
        Alfonso Rodriguez-Molares <alfonso.r.molares@ntnu.no>
    """

    # Compulsory properties
    @compulsory_property
    def points(self) -> np.ndarray:
        "Matrix of point scaterers [x y z Gamma] - [m m m unitless]"
        return LazyArray(self._reader["points"])

    @compulsory_property
    def time(self) -> float:
        "Time [s]"
        return LazyScalar(self._reader["time"])

    @compulsory_property
    def sound_speed(self) -> float:
        "Medium sound speed [m/s]"
        return LazyScalar(self._reader["sound_speed"])

    @compulsory_property
    def density(self) -> float:
        "Medium density [kg/m3]"
        return LazyScalar(self._reader["density"])

    @compulsory_property
    def alpha(self) -> float:
        "Medium attenuation [dB/cm/MHz]"
        return LazyScalar(self._reader["alpha"])

    # Dependent properties
    @dependent_property
    def N_points(self) -> int:
        "Number of points"
        return self.points.shape[0]

    @dependent_property
    def x(self) -> np.ndarray:
        "Points position in the x axis [m]"
        return self.points[:, 0]

    @dependent_property
    def y(self) -> np.ndarray:
        "Points position in the y axis [m]"
        return self.points[:, 1]

    @dependent_property
    def z(self) -> np.ndarray:
        "Points position in the z axis [m]"
        return self.points[:, 2]

    @dependent_property
    def Gamma(self) -> np.ndarray:
        "Reflection coefficient [unitless]"
        return self.points[:, 3]

    @dependent_property
    def r(self) -> np.ndarray:
        "Distance from the points to the origin [m]"
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    @dependent_property
    def theta(self) -> np.ndarray:
        "Angle in the azimuth direction respect to origin [rad]"
        return np.arctan2(self.x, self.z)

    @dependent_property
    def phi(self) -> np.ndarray:
        "Angle in the elevation direction respect to origin [rad]"
        return np.arctan2(self.y, self.z)
