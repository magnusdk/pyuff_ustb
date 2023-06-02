from functools import cached_property

import numpy as np

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray, LazyScalar, util


class Wave(PyuffObject):
    @cached_property
    def wavefront(self):
        from pyuff.objects.wavefront import Wavefront

        with self._reader.h5_obj as h5_obj:
            if "wavefront" in h5_obj:
                return Wavefront(np.squeeze(h5_obj["wavefront"][:]))
        return Wavefront.spherical

    @cached_property
    def source(self):
        from pyuff.objects.point import Point

        return Point(self._reader["source"])

    @cached_property
    def origin(self):
        from pyuff.objects.point import Point

        return Point(self._reader["origin"])

    @cached_property
    def apodization(self):
        if "apodization" in self._reader:
            from pyuff.objects.apodization import Apodization

            return Apodization(self._reader["apodization"])

    # Optional properties
    @cached_property
    def probe(self):
        if "probe" in self._reader:
            return util.read_probe(self._reader["probe"])

    @cached_property
    def event(self):
        "Index of the transmit/receive event this wave refers to"
        if "event" in self._reader:
            return LazyScalar(self._reader["event"])

    @cached_property
    def delay(self):
        "Time interval between t0 and acquistion start [s]"
        if "delay" in self._reader:
            return LazyScalar(self._reader["delay"])
        return 0.0

    @cached_property
    def sound_speed(self):
        "Reference speed of sound [m/s]"
        if "sound_speed" in self._reader:
            return LazyScalar(self._reader["sound_speed"])
        return 1540.0
