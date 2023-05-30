from functools import cached_property

from pyuff.objects import PyuffObject
from pyuff.readers import LazyArray


class Point(PyuffObject):
    @cached_property
    def distance(self):
        return LazyArray(self._reader["distance"])

    @cached_property
    def azimuth(self):
        return LazyArray(self._reader["azimuth"])

    @cached_property
    def elevation(self):
        return LazyArray(self._reader["elevation"])
