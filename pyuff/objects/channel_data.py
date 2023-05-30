from functools import cached_property

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray, util


class ChannelData(PyuffObject):
    @cached_property
    def sampling_frequency(self):
        return LazyArray(self._reader["sampling_frequency"])

    @cached_property
    def initial_time(self):
        return LazyArray(self._reader["initial_time"])

    @cached_property
    def sound_speed(self):
        return LazyArray(self._reader["sound_speed"])

    @cached_property
    def modulation_frequency(self):
        return LazyArray(self._reader["modulation_frequency"])

    @cached_property
    def sequence(self):
        return util.read_sequence(self._reader["sequence"])

    @cached_property
    def probe(self):
        from pyuff.objects.probe import Probe

        return Probe(self._reader["probe"])

    @cached_property
    def data(self):
        return LazyArray(self._reader["data"])

    # Optional properties
    @cached_property
    def pulse(self):
        from pyuff.objects.pulse import Pulse

        reader = self._reader["pulse"]
        return Pulse(reader) if reader else None

    @cached_property
    def phantom(self):
        from pyuff.objects.phantom import Phantom

        reader = self._reader["phantom"]
        return Phantom(reader) if reader else None

    @cached_property
    def PRF(self):
        reader = self._reader["PRF"]
        return LazyArray(reader) if reader else None
