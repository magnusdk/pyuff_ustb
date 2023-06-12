from pyuff.objects.uff import (
    Uff,
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff.readers import LazyArray, LazyScalar, util


class BeamformedData(Uff):
    # Compulsory properties
    @compulsory_property
    def scan(self):
        "SCAN object or array of SCAN objects"
        return util.read_scan(self._reader["scan"])

    @compulsory_property
    def data(self):
        "Data [pixel x channel x wave x frame]"
        return LazyArray(self._reader["data"])

    # Optional properties
    @optional_property
    def phantom(self):
        "PHANTOM object"
        from pyuff.objects.phantom import Phantom

        return Phantom(self._reader["phantom"])

    @optional_property
    def sequence(self):
        "Array of WAVE objects"
        from pyuff.objects.wave import Wave

        return util.read_potentially_list(self._reader["sequence"], Wave)

    @optional_property
    def probe(self):
        "PROBE object"
        from pyuff.objects.probes.probe import Probe

        return Probe(self._reader["probe"])

    @optional_property
    def pulse(self):
        "PULSE object"
        from pyuff.objects import Pulse

        return Pulse(self._reader["pulse"])

    @optional_property
    def sampling_frequency(self):
        "Sampling frequency in the depth direction in [Hz]"
        return LazyScalar(self._reader["sampling_frequency"])

    @optional_property
    def modulation_frequency(self):
        "Modulation frequency in [Hz]"
        return LazyScalar(self._reader["modulation_frequency"])

    @optional_property
    def frame_rate(self):
        "Framerate for Video or GIF file to be saved [fps]"
        return LazyScalar(self._reader["frame_rate"])

    @dependent_property
    def N_pixels(self):
        "Number of pixels"
        return self.data.shape[0]

    @dependent_property
    def N_channels(self):
        "Number of channels"
        return self.data.shape[1]

    @dependent_property
    def N_waves(self):
        "Number of waves (transmit events)"
        return self.data.shape[2]

    @dependent_property
    def N_frames(self):
        "Number of frames"
        return self.data.shape[3]
