from pyuff.objects.uff import compulsory_property, optional_property
from pyuff.objects.probe import Probe
from pyuff.readers import LazyScalar


class LinearArray(Probe):
    # Compulsory properties
    @compulsory_property
    def N(self):
        "Number of elements"
        return LazyScalar(self._reader["N"])

    @compulsory_property
    def pitch(self):
        "Distance between the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["pitch"])

    # Optional properties
    @optional_property
    def element_width(self):
        "Width of the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["element_width"])

    @optional_property
    def element_height(self):
        "Height of the elements in the elevation direction [m]"
        return LazyScalar(self._reader["element_height"])
