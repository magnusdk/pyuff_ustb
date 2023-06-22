import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property, dependent_property
from pyuff_ustb.readers import LazyArray


class Scan(Uff):
    # Compulsory properties
    @compulsory_property
    def x(self) -> np.ndarray:
        "Vector containing the x coordinates of each pixel in [m]"
        return LazyArray(self._reader["x"])

    @compulsory_property
    def y(self) -> np.ndarray:
        "Vector containing the y coordinates of each pixel in [m]"
        return LazyArray(self._reader["y"])

    @compulsory_property
    def z(self) -> np.ndarray:
        "Vector containing the z coordinates of each pixel in [m]"
        return LazyArray(self._reader["z"])

    # Dependent properties
    @dependent_property
    def xyz(self) -> np.ndarray:
        "Vector containing the [x, y, z] coordinates of each pixel in [m]"
        return np.stack([self.x, self.y, self.z], axis=-1)
