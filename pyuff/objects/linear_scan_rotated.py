from functools import cached_property

from pyuff.objects.scan import Scan
from pyuff.readers import LazyArray, LazyScalar


class LinearScanRotated(Scan):
    @cached_property
    def x_axis(self):
        return LazyArray(self._reader["x_axis"])

    @cached_property
    def z_axis(self):
        return LazyArray(self._reader["z_axis"])

    @cached_property
    def rotation_angle(self):
        return LazyScalar(self._reader["rotation_angle"])

    @cached_property
    def center_of_rotation(self):
        return LazyArray(self._reader["center_of_rotation"])
