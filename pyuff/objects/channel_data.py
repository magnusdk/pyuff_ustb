from pyuff.objects.uff import (
    Uff,
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff.readers import LazyArray, LazyScalar, util


class ChannelData(Uff):
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
        from pyuff.objects.wave import Wave

        return util.read_potentially_list(self._reader["sequence"], Wave)

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
    def PRF(self):
        prf_key = "PRF" if "PRF" in self._reader else "prf"
        return LazyScalar(self._reader[prf_key])

    @optional_property
    def N_active_elements(self):
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
        from pyuff.objects.wave import Wave

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
