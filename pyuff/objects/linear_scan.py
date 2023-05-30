from functools import cached_property

from pyuff.objects.scan import Scan
from pyuff.readers import LazyArray


class LinearScan(Scan):
    @cached_property
    def x_axis(self):
        return LazyArray(self._reader["x_axis"])

    @cached_property
    def z_axis(self):
        return LazyArray(self._reader["z_axis"])
