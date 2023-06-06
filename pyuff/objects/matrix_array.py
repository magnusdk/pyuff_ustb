from pyuff.objects.base import compulsory_property, optional_property
from pyuff.objects.probe import Probe
from pyuff.readers import LazyScalar


class MatrixArray(Probe):
    # Compulsory properties
    @compulsory_property
    def pitch_x(self):
        "Distance between the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["pitch_x"])

    @compulsory_property
    def pitch_y(self):
        "Distance between the elements in the elevation direction [m]"
        return LazyScalar(self._reader["pitch_y"])

    @compulsory_property
    def N_x(self):
        "Number of elements in the azimuth direction"
        return LazyScalar(self._reader["N_x"])

    @compulsory_property
    def N_y(self):
        "Number of elements in the elevation direction"
        return LazyScalar(self._reader["N_y"])

    # Optional properties
    @optional_property
    def element_width(self):
        "Width of the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["element_width"])

    @optional_property
    def element_height(self):
        "Height of the elements in the elevation direction [m]"
        return LazyScalar(self._reader["element_height"])
