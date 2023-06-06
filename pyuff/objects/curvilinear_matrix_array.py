from pyuff.objects.base import compulsory_property, optional_property
from pyuff.objects.matrix_array import MatrixArray
from pyuff.readers import LazyScalar


class CurvilinearMatrixArray(MatrixArray):
    # Compulsory properties
    @compulsory_property
    def radius_x(self):
        "Radius of the curvilinear array in azimuth direction [m]"
        return LazyScalar(self._reader["radius_x"])

    # Optional properties
    @optional_property
    def maximum_angle(self):
        "Angle of the outermost elements in the array"
        # TODO
