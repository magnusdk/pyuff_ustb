from functools import cached_property

from pyuff.objects.scan import Scan
from pyuff.readers import LazyArray


class Linear3DScan(Scan):
    @cached_property
    def radial_axis(self):
        return LazyArray(self._reader["radial_axis"])

    @cached_property
    def axial_axis(self):
        return LazyArray(self._reader["axial_axis"])

    @cached_property
    def roll(self):
        return LazyArray(self._reader["roll"])
