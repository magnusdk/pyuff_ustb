from functools import cached_property

from pyuff.objects.base import PyuffObject
from pyuff.readers import LazyArray, LazyScalar, util


class ChannelData(PyuffObject):
    @cached_property
    def sampling_frequency(self):
        return LazyScalar(self._reader["sampling_frequency"])

    @cached_property
    def initial_time(self):
        return LazyScalar(self._reader["initial_time"])

    @cached_property
    def sound_speed(self):
        return LazyScalar(self._reader["sound_speed"])

    @cached_property
    def modulation_frequency(self):
        return LazyScalar(self._reader["modulation_frequency"])

    @cached_property
    def sequence(self):
        return util.read_sequence(self._reader["sequence"])

    @cached_property
    def probe(self):
        return util.read_probe(self._reader["probe"])

    @cached_property
    def data(self):
        return LazyArray(self._reader["data"]).T

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
    def prf(self):
        reader = self._reader["PRF"]
        return LazyScalar(reader) if reader else None

    # Dependent properties
    @property
    def n_samples(self) -> int:
        "Number of samples in the data"
        return self.data.shape[0]

    @property
    def n_elements(self) -> int:
        "Number of elements in the probe"
        return self.probe.n_elements

    @property
    def n_channels(self) -> int:
        "Number of elements in the probe"
        return self.probe.n_elements

    @property
    def n_waves(self) -> int:
        "Number of transmitted waves"
        from pyuff.objects.wave import Wave

        if isinstance(self.sequence, list):
            return len(self.sequence)
        if isinstance(self.sequence, Wave):
            return 1
        return 0

    @property
    def n_frames(self) -> int:
        "Number of frames"
        if self.data.ndim == 4:
            return self.data.shape[3]
        return 1

    @property
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
