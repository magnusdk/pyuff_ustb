from pyuff.objects.uff import (
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff.objects.probe import Probe
from pyuff.readers import LazyScalar


class CurvilinearArray(Probe):
    # Compulsory properties
    @compulsory_property
    def N(self):
        "Number of elements"
        return LazyScalar(self._reader["N"])

    @compulsory_property
    def pitch(self):
        "Distance between the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["pitch"])

    @compulsory_property
    def radius(self):
        "Radius of the curvilinear array [m]"
        return LazyScalar(self._reader["radius"])

    # Optional properties
    @optional_property
    def element_width(self):
        "Width of the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["element_width"])

    @optional_property
    def element_height(self):
        "Height of the elements in the elevation direction [m]"
        return LazyScalar(self._reader["element_height"])

    # Dependent properties
    @dependent_property
    def maximum_angle(self):
        "Angle of the outermost elements in the array"
        ...  # TODO
