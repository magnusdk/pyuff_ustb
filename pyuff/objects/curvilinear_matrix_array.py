from functools import cached_property

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray


class CurvilinearMatrixArray(PyuffObject):
    @cached_property
    def radius_x(self):
        return LazyArray(self._reader["radius_x"])
