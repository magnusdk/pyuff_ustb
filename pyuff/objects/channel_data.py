from pyuff.objects.base import (
    PyuffObject,
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff.readers import LazyArray, LazyScalar, util


class ChannelData(PyuffObject):
    # Compulsory properties
    @compulsory_property
    def sampling_frequency(self):
        return LazyScalar(self._reader["sampling_frequency"])

    @compulsory_property
    def initial_time(self):
        return LazyScalar(self._reader["initial_time"])

    @compulsory_property
    def sound_speed(self):
        return LazyScalar(self._reader["sound_speed"])

    @compulsory_property
    def modulation_frequency(self):
        return LazyScalar(self._reader["modulation_frequency"])

    @compulsory_property
    def sequence(self):
        return util.read_sequence(self._reader["sequence"])

    @compulsory_property
    def probe(self):
        return util.read_probe(self._reader["probe"])

    @compulsory_property
    def data(self):
        return LazyArray(self._reader["data"]).T

    # Optional properties
    @optional_property
    def pulse(self):
        from pyuff.objects.pulse import Pulse

        return Pulse(self._reader["pulse"])

    @optional_property
    def phantom(self):
        from pyuff.objects.phantom import Phantom

        return Phantom(self._reader["phantom"])

    @optional_property
    def prf(self):
        return LazyScalar(self._reader["PRF"])

    # Dependent properties
    @dependent_property
    def n_samples(self) -> int:
        "Number of samples in the data"
        return self.data.shape[0]

    @dependent_property
    def n_elements(self) -> int:
        "Number of elements in the probe"
        return self.probe.n_elements

    @dependent_property
    def n_channels(self) -> int:
        "Number of elements in the probe"
        return self.probe.n_elements

    @dependent_property
    def n_waves(self) -> int:
        "Number of transmitted waves"
        from pyuff.objects.wave import Wave

        if isinstance(self.sequence, list):
            return len(self.sequence)
        if isinstance(self.sequence, Wave):
            return 1
        return 0

    @dependent_property
    def n_frames(self) -> int:
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
