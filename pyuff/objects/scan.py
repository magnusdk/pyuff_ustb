from functools import cached_property

from pyuff.objects import PyuffObject
from pyuff.readers import LazyArray


class Scan(PyuffObject):
    @cached_property
    def xyz(self) -> LazyArray:
        return LazyArray(self._reader["xyz"])
