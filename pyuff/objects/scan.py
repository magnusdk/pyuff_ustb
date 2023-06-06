import numpy as np

from pyuff.objects import PyuffObject
from pyuff.objects.base import PyuffObject, compulsory_property, dependent_property
from pyuff.readers import LazyArray


class Scan(PyuffObject):
    # Compulsory properties
    @compulsory_property
    def x(self) -> LazyArray:
        return LazyArray(self._reader["x"])

    @compulsory_property
    def y(self) -> LazyArray:
        return LazyArray(self._reader["y"])

    @compulsory_property
    def z(self) -> LazyArray:
        return LazyArray(self._reader["z"])

    # Dependent properties
    @dependent_property
    def xyz(self):
        return np.stack([self.x, self.y, self.z], axis=-1)
