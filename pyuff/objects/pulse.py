from functools import cached_property

from pyuff.objects import PyuffObject
from pyuff.readers import LazyArray


class Pulse(PyuffObject):
    @cached_property
    def center_frequency(self) -> LazyArray:
        return LazyArray(self._reader["center_frequency"])

    @cached_property
    def fractional_bandwidth(self) -> LazyArray:
        return LazyArray(self._reader["fractional_bandwidth"])

    @cached_property
    def phase(self) -> LazyArray:
        return LazyArray(self._reader["phase"])

    @cached_property
    def waveform(self) -> LazyArray:
        return LazyArray(self._reader["waveform"])
