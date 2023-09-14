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
    from pyuff_ustb.objects.phantom import Phantom
    from pyuff_ustb.objects.probes.probe import Probe
    from pyuff_ustb.objects.pulse import Pulse
    from pyuff_ustb.objects.wave import Wave

    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class ChannelData(Uff):
    """:class:`Uff` class to hold channel data.

    :class:`ChannelData` contains raw ultrasound data as acquired from an ultrasound
    scanner. Data is stored in the property :attr:`data` with dimensions:
    ``[time-dimension x channel-dimension x wave-dimension x frame-dimension]``.

    Original authors:
        Alfonso Rodriguez-Molares <alfonso.r.molares@ntnu.no>
    """

    # Compulsory properties
    @compulsory_property
    def sampling_frequency(self) -> float:
        "Sampling frequency [Hz]"
        return LazyScalar(self._reader["sampling_frequency"])

    @compulsory_property
    def initial_time(self) -> float:
        "Time of the initial sample [s]"
        return LazyScalar(self._reader["initial_time"])

    @compulsory_property
    def sound_speed(self) -> float:
        "Reference sound speed [m/s]"
        return LazyScalar(self._reader["sound_speed"])

    @compulsory_property
    def modulation_frequency(self) -> float:
        "Modulation frequency [Hz]"
        return LazyScalar(self._reader["modulation_frequency"])

    @compulsory_property
    def sequence(self) -> Union["Wave", List["Wave"]]:
        "Collection of UFF.WAVE objects"
        from pyuff_ustb.objects.wave import Wave

        return util.read_potentially_list(self._reader["sequence"], Wave)

    @compulsory_property
    def probe(self) -> "Probe":
        "UFF.PROBE object"
        return util.read_probe(self._reader["probe"])

    @compulsory_property
    def data(self) -> np.ndarray:
        "Channel data [time dim. x channel dim. x wave dim. x frame dim.]"
        return LazyArray(self._reader["data"]).T

    # Optional properties
    @optional_property
    def pulse(self) -> "Pulse":
        "UFF.PULSE object"
        from pyuff_ustb.objects.pulse import Pulse

        return Pulse(self._reader["pulse"])

    @optional_property
    def phantom(self) -> "Phantom":
        "UFF.PHANTOM object"
        from pyuff_ustb.objects.phantom import Phantom

        return Phantom(self._reader["phantom"])

    @optional_property
    def PRF(self) -> float:
        "Pulse repetition frequency [Hz]"
        prf_key = "PRF" if "PRF" in self._reader else "prf"
        return LazyScalar(self._reader[prf_key])

    @optional_property
    def N_active_elements(self) -> int:
        "Number of active transducers on receive"
        return LazyScalar(self._reader["N_active_elements"])

    # Dependent properties
    @dependent_property
    def N_samples(self) -> int:
        "Number of samples in the data"
        return self.data.shape[0]

    @dependent_property
    def N_elements(self) -> int:
        "Number of elements in the probe"
        return self.probe.N_elements

    @dependent_property
    def N_channels(self) -> int:
        "Number of elements in the probe"
        return self.probe.N_elements

    @dependent_property
    def N_waves(self) -> int:
        "Number of transmitted waves"
        from pyuff_ustb.objects.wave import Wave

        if isinstance(self.sequence, list):
            return len(self.sequence)
        if isinstance(self.sequence, Wave):
            return 1
        return 0

    @dependent_property
    def N_frames(self) -> int:
        "Number of frames"
        if self.data.ndim == 4:
            return self.data.shape[3]
        return 1

    @dependent_property
    def wavelength(self) -> float:
        """Wavelength [m]

        Same as ChannelData.lambda in USTB, but lambda is a reserved keyword in Python.
        """
        assert (
            self.sound_speed is not None
        ), "You need to set the channel_data.sound_speed"
        assert (
            self.pulse is not None
            and self.pulse.center_frequency is not None
            and self.pulse.center_frequency != 0
        ), "You need to set the pulse and the pulse center frequency."
        return self.sound_speed / self.pulse.center_frequency

    def _preprocess_write(self, name: str, value):
        if name == "data":
            return value.T
        return value
