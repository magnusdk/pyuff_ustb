from functools import cached_property

from pyuff.objects.probe import Probe
from pyuff.readers import LazyScalar


class CurvilinearArray(Probe):
    @cached_property
    def N(self):
        "Number of elements"
        return LazyScalar(self._reader["N"])

    @cached_property
    def pitch(self):
        "Distance between the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["pitch"])

    @cached_property
    def radius(self):
        "Radius of the curvilinear array [m]"
        return LazyScalar(self._reader["radius"])

    # Optional
    @cached_property
    def element_width(self):
        return LazyScalar(self._reader["element_width"])

    @cached_property
    def element_height(self):
        return LazyScalar(self._reader["element_height"])
