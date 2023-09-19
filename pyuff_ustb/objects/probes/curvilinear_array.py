from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.probes.probe import Probe
from pyuff_ustb.objects.uff import (
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff_ustb.readers import LazyScalar

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class CurvilinearArray(Probe):
    """:class:`Uff` class to define a curvilinear array probe geometry.

    :class:`CurvilinearArray` defines a array of regularly space elements on an arc in
    the azimuth dimensions. Optionally it can hold each element width and height,
    assuming the elements are rectangular.

    Original authors:
        Alfonso Rodriguez-Molares (alfonsom@ntnu.no)
    """

    # Compulsory properties
    @compulsory_property
    def N(self) -> int:
        "Number of elements"
        return LazyScalar(self._reader["N"])

    @compulsory_property
    def pitch(self) -> float:
        "Distance between the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["pitch"])

    @compulsory_property
    def radius(self) -> float:
        "Radius of the curvilinear array [m]"
        return LazyScalar(self._reader["radius"])

    # Optional properties
    @optional_property
    def element_width(self) -> float:
        "Width of the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["element_width"])

    @optional_property
    def element_height(self) -> float:
        "Height of the elements in the elevation direction [m]"
        return LazyScalar(self._reader["element_height"])

    # Dependent properties
    @dependent_property
    def maximum_angle(self) -> float:
        "Angle of the outermost elements in the array"
        return np.max(np.abs(self.theta))

    # Override some compulsory properties of Probe
    @dependent_property
    def geometry(self) -> np.ndarray:
        element_width = (
            self.element_width if self.element_width is not None else self.pitch
        )
        element_height = (
            self.element_height
            if self.element_height is not None
            else 10 * element_width
        )

        # Compute element coordinates
        dtheta = 2 * np.arcsin(self.pitch / 2 / self.radius)
        theta = np.arange(0, self.N) * dtheta
        theta = theta - np.mean(theta)
        x0 = self.radius * np.sin(theta)
        z0 = self.radius * np.cos(theta) - self.radius

        return np.array(
            [
                x0,
                np.zeros(self.N),
                z0,
                theta,
                np.zeros(self.N),
                element_width * np.ones(self.N),
                element_height * np.ones(self.N),
            ]
        )
