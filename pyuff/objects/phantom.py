from functools import cached_property

from pyuff.objects import PyuffObject
from pyuff.readers import LazyArray


class Phantom(PyuffObject):
    @cached_property
    def points(self):
        return LazyArray(self._reader["points"])

    @cached_property
    def time(self):
        return LazyArray(self._reader["time"])

    @cached_property
    def sound_speed(self):
        return LazyArray(self._reader["sound_speed"])

    @cached_property
    def density(self):
        return LazyArray(self._reader["density"])

    @cached_property
    def alpha(self):
        return LazyArray(self._reader["alpha"])
