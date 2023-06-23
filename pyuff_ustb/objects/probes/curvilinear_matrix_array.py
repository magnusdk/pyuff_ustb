import numpy as np

from pyuff_ustb.objects.probes.matrix_array import MatrixArray
from pyuff_ustb.objects.uff import compulsory_property, dependent_property
from pyuff_ustb.readers import LazyScalar


class CurvilinearMatrixArray(MatrixArray):
    """:class:`Uff` class to define a curvilinear matrix array probe geometry.

    :class:`CurvilinearMatrixArray` defines a array of regularly space elements on an 
    arc in the azimuth dimensions and linear in elevation direction. Optionally it can 
    hold each element width and height, assuming the elements are rectangular.

    Original authors:
        Anders E. Vrålstad (anders.e.vralstad@ntnu.no)
    """

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
