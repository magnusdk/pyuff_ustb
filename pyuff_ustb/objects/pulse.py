import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property
from pyuff_ustb.readers import LazyArray, LazyScalar


class Pulse(Uff):
    # Compulsory properties
    @compulsory_property
    def center_frequency(self) -> float:
        "Center frequency [Hz]"
        return LazyScalar(self._reader["center_frequency"])

    @compulsory_property
    def fractional_bandwidth(self) -> float:
        "Probe fractional bandwidth [unitless]"
        return LazyScalar(self._reader["fractional_bandwidth"])

    @compulsory_property
    def phase(self) -> float:
        "Initial phase [rad]"
        return LazyScalar(self._reader["phase"])

    @compulsory_property
    def waveform(self) -> np.ndarray:
        "Transmitted waveform (for example used for match filtering)"
        return LazyArray(self._reader["waveform"])
