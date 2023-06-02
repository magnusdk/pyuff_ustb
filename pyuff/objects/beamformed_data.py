from functools import cached_property

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray, LazyScalar


class BeamformedData(PyuffObject):
    @cached_property
    def scan(self):
        from pyuff.objects.scan import Scan

        return Scan(self._reader["scan"])

    @cached_property
    def data(self):
        return LazyArray(self._reader["sound_speed"])

    # Optional properties
    @cached_property
    def phantom(self):
        ...

    @cached_property
    def sequence(self):
        ...

    @cached_property
    def probe(self):
        ...

    @cached_property
    def pulse(self):
        ...

    @cached_property
    def sampling_frequency(self):
        return LazyScalar(self._reader["sampling_frequency"])

    @cached_property
    def modulation_frequency(self):
        return LazyScalar(self._reader["modulation_frequency"])
