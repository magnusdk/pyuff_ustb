import numpy as np

from pyuff_ustb.objects.probes.matrix_array import MatrixArray
from pyuff_ustb.objects.uff import compulsory_property, dependent_property
from pyuff_ustb.readers import LazyScalar


class CurvilinearMatrixArray(MatrixArray):
    # Compulsory properties
    @compulsory_property
    def radius_x(self) -> float:
        "Radius of the curvilinear array in azimuth direction [m]"
        return LazyScalar(self._reader["radius_x"])

    # Dependent properties
    @dependent_property
    def maximum_angle(self) -> float:
        "Angle of the outermost elements in the array"
        return np.max(np.abs(self.theta))
