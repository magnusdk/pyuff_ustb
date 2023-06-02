from functools import cached_property

from pyuff.objects.probe import Probe
from pyuff.readers import LazyScalar


class LinearArray(Probe):
    @cached_property
    def N(self):
        return LazyScalar(self._reader["N"])

    @cached_property
    def pitch(self):
        return LazyScalar(self._reader["pitch"])

    # Optional
    @cached_property
    def element_width(self):
        return LazyScalar(self._reader["element_width"])

    @cached_property
    def element_height(self):
        return LazyScalar(self._reader["element_height"])
