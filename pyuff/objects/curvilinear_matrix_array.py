from functools import cached_property

from pyuff.objects.matrix_array import MatrixArray
from pyuff.readers import LazyScalar


class CurvilinearMatrixArray(MatrixArray):
    @cached_property
    def radius_x(self):
        return LazyScalar(self._reader["radius_x"])
