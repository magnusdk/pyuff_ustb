from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.uff import (
    Uff,
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff_ustb.readers import LazyScalar, util

if TYPE_CHECKING:
    from pyuff_ustb.objects.apodization import Apodization
    from pyuff_ustb.objects.point import Point
    from pyuff_ustb.objects.probes.probe import Probe
    from pyuff_ustb.objects.wavefront import Wavefront


class Wave(Uff):
    # Compulsory properties
    @compulsory_property
    def wavefront(self) -> "Wavefront":
        "WAVEFRONT enumeration class"
        from pyuff_ustb.objects.wavefront import Wavefront

        if "wavefront" in self._reader:
            return util.read_enum(self._reader["wavefront"], Wavefront)
        return Wavefront.spherical

    @compulsory_property
    def source(self) -> "Point":
        "POINT class"
        from pyuff_ustb.objects.point import Point

        return Point(self._reader["source"])

    @compulsory_property
    def origin(self) -> "Point":
        "POINT class"
        from pyuff_ustb.objects.point import Point

        return Point(self._reader["origin"])

    @compulsory_property
    def apodization(self) -> "Apodization":
        "APODIZATION class"
        from pyuff_ustb.objects.apodization import Apodization

        return Apodization(self._reader["apodization"])

    # Optional properties
    @optional_property
    def probe(self) -> "Probe":
        return util.read_probe(self._reader["probe"])

    @optional_property
    def event(self) -> int:
        "Index of the transmit/receive event this wave refers to"
        return LazyScalar(self._reader["event"])

    @optional_property
    def delay(self) -> float:
        "Time interval between t0 and acquistion start [s]"
        if "delay" in self._reader:
            return LazyScalar(self._reader["delay"])
        return 0.0

    @optional_property
    def sound_speed(self) -> float:
        "Reference speed of sound [m/s]"
        if "sound_speed" in self._reader:
            return LazyScalar(self._reader["sound_speed"])
        return 1540.0

    # Dependent properties
    @dependent_property
    def N_elements(self) -> int:
        "Number of elements"
        return self.probe.N_elements

    @dependent_property
    def delay_values(self):
        "Delay [s]"
        raise NotImplementedError(
            "Delay value computation is outside the scope of pyuff_ustb"
        )

    @dependent_property
    def apodization_values(self):
        "Apodization [unitless]"
        raise NotImplementedError(
            "Apodization computation is outside the scope of pyuff_ustb"
        )
