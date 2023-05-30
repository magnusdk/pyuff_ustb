from functools import cached_property

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray


class Probe(PyuffObject):

    @cached_property
    def geometry(self):
        return LazyArray(self._reader["origin"])
    
    @cached_property
    def origin(self):
        from pyuff.objects.point import Point

        if "origin" in self._reader:
            return Point(self._reader["origin"])
