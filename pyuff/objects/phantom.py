from functools import cached_property

from pyuff.objects import PyuffObject
from pyuff.readers import LazyArray, LazyScalar


class Phantom(PyuffObject):
    @cached_property
    def points(self):
        return LazyArray(self._reader["points"])

    @cached_property
    def time(self):
        return LazyScalar(self._reader["time"])

    @cached_property
    def sound_speed(self):
        return LazyScalar(self._reader["sound_speed"])

    @cached_property
    def density(self):
        return LazyScalar(self._reader["density"])

    @cached_property
    def alpha(self):
        return LazyScalar(self._reader["alpha"])
