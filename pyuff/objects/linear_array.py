from functools import cached_property

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray


class LinearArray(PyuffObject):
    @cached_property
    def N(self):
        return LazyArray(self._reader["N"])

    @cached_property
    def pitch(self):
        return LazyArray(self._reader["pitch"])

    # Optional
    @cached_property
    def element_width(self):
        return LazyArray(self._reader["element_width"])

    @cached_property
    def element_height(self):
        return LazyArray(self._reader["element_height"])
