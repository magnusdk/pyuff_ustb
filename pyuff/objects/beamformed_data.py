from pyuff.objects.base import PyuffObject, compulsory_property, optional_property
from pyuff.readers import LazyArray, util


class BeamformedData(PyuffObject):
    # Compulsory properties
    @compulsory_property
    def scan(self):
        return util.read_scan(self._reader["scan"])

    @compulsory_property
    def data(self):
        return LazyArray(self._reader["sound_speed"])

    @optional_property
    def phantom(self):
        ...  # TODO

    # Optional properties
    @optional_property
    def sequence(self):
        ...  # TODO

    @optional_property
    def probe(self):
        ...  # TODO

    @optional_property
    def pulse(self):
        ...  # TODO

    @optional_property
    def sampling_frequency(self):
        ...  # TODO

    @optional_property
    def modulation_frequency(self):
        ...  # TODO

    @optional_property
    def frame_rate(self):
        ...  # TODO
