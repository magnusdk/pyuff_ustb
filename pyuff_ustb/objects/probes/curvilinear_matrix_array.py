from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.probes.matrix_array import MatrixArray
from pyuff_ustb.objects.uff import compulsory_property, dependent_property
from pyuff_ustb.readers import LazyScalar

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


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

    # Override some compulsory properties of Probe
    @dependent_property
    def geometry(self) -> np.ndarray:
        element_width = self.pitch_x
        element_height = self.pitch_y

        # Compute element coordinates
        dtheta = 2 * np.arcsin(self.pitch_x / 2 / self.radius_x)
        theta = np.arange(0, self.N_x) * dtheta
        theta = theta - np.mean(theta)
        x0 = self.radius_x * np.sin(theta)
        y0 = np.arange(0, self.N_y) * self.pitch_y
        y0 = y0 - np.mean(y0)

        X, Y = np.meshgrid(x0, y0)
        Z = self.radius_x * np.ones((self.N_y, 1)) * np.cos(theta) - self.radius_x
        THETA = np.arctan2(X, Z) - np.pi / 2

        return np.array(
            [
                X,
                Y,
                Z,
                THETA,
                np.zeros(self.N_x * self.N_y),
                element_width * np.ones(self.N_x * self.N_y),
                element_height * np.ones(self.N_x * self.N_y),
            ]
        )
