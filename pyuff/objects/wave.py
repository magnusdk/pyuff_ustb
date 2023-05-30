from functools import cached_property

import numpy as np
from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray


class Wave(PyuffObject):
    @cached_property
    def wavefront(self):
        from pyuff.objects.wavefront import wavefront

        with self._reader.h5_obj as h5_obj:
            if "wavefront" in h5_obj:
                return wavefront(np.squeeze(h5_obj["wavefront"][:]))

    @cached_property
    def source(self):
        from pyuff.objects.point import Point

        return Point(self._reader["source"])

    @cached_property
    def apodization(self):
        if "apodization" in self._reader:
            from pyuff.objects.apodization import Apodization

            return Apodization(self._reader["apodization"])

    # Optional properties
    @cached_property
    def probe(self):
        from pyuff.objects.probe import Probe

        return Probe(self._reader["probe"])

    @cached_property
    def event(self):
        return LazyArray(self._reader["event"])

    @cached_property
    def initial_time(self):
        return LazyArray(self._reader["initial_time"])

    @cached_property
    def sound_speed(self) -> float:
        return LazyArray(self._reader["sound_speed"])
