from functools import cached_property

from pyuff.objects import PyuffObject
from pyuff.readers import LazyArray, LazyScalar


class Pulse(PyuffObject):
    @cached_property
    def center_frequency(self):
        return LazyScalar(self._reader["center_frequency"])

    @cached_property
    def fractional_bandwidth(self):
        return LazyScalar(self._reader["fractional_bandwidth"])

    @cached_property
    def phase(self):
        return LazyScalar(self._reader["phase"])

    @cached_property
    def waveform(self):
        return LazyArray(self._reader["waveform"])
