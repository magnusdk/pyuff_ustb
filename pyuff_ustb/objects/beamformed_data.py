from typing import TYPE_CHECKING, List, Union

import numpy as np

from pyuff_ustb.objects.uff import (
    Uff,
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff_ustb.readers import LazyArray, LazyScalar, util

if TYPE_CHECKING:
    from pyuff_ustb.objects import Pulse
    from pyuff_ustb.objects.phantom import Phantom
    from pyuff_ustb.objects.probes.probe import Probe
    from pyuff_ustb.objects.scans.scan import Scan
    from pyuff_ustb.objects.wave import Wave


class BeamformedData(Uff):
    # Compulsory properties
    @compulsory_property
    def scan(self) -> "Scan":
        "SCAN object or array of SCAN objects"
        return util.read_scan(self._reader["scan"])

    @compulsory_property
    def data(self) -> np.ndarray:
        "Data [pixel x channel x wave x frame]"
        return LazyArray(self._reader["data"])

    # Optional properties
    @optional_property
    def phantom(self) -> "Phantom":
        "PHANTOM object"
        from pyuff_ustb.objects.phantom import Phantom

        return Phantom(self._reader["phantom"])

    @optional_property
    def sequence(self) -> Union["Wave", List["Wave"]]:
        "Array of WAVE objects"
        from pyuff_ustb.objects.wave import Wave

        return util.read_potentially_list(self._reader["sequence"], Wave)

    @optional_property
    def probe(self) -> "Probe":
        "PROBE object"
        from pyuff_ustb.objects.probes.probe import Probe

        return Probe(self._reader["probe"])

    @optional_property
    def pulse(self) -> "Pulse":
        "PULSE object"
        from pyuff_ustb.objects import Pulse

        return Pulse(self._reader["pulse"])

    @optional_property
    def sampling_frequency(self) -> float:
        "Sampling frequency in the depth direction in [Hz]"
        return LazyScalar(self._reader["sampling_frequency"])

    @optional_property
    def modulation_frequency(self) -> float:
        "Modulation frequency in [Hz]"
        return LazyScalar(self._reader["modulation_frequency"])

    @optional_property
    def frame_rate(self) -> int:
        "Framerate for Video or GIF file to be saved [fps]"
        return LazyScalar(self._reader["frame_rate"])

    @dependent_property
    def N_pixels(self) -> int:
        "Number of pixels"
        return self.data.shape[0]

    @dependent_property
    def N_channels(self) -> int:
        "Number of channels"
        return self.data.shape[1]

    @dependent_property
    def N_waves(self) -> int:
        "Number of waves (transmit events)"
        return self.data.shape[2]

    @dependent_property
    def N_frames(self) -> int:
        "Number of frames"
        return self.data.shape[3]
