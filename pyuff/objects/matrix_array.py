from functools import cached_property

from pyuff.objects.probe import Probe
from pyuff.readers import LazyScalar


class MatrixArray(Probe):
    @cached_property
    def pitch_x(self):
        return LazyScalar(self._reader["pitch_x"])

    @cached_property
    def pitch_y(self):
        return LazyScalar(self._reader["pitch_y"])

    @cached_property
    def N_x(self):
        return LazyScalar(self._reader["N_x"])

    @cached_property
    def N_y(self):
        return LazyScalar(self._reader["N_y"])

    # Optional
    @cached_property
    def element_width(self):
        return LazyScalar(self._reader["element_width"])

    @cached_property
    def element_height(self):
        return LazyScalar(self._reader["element_height"])
