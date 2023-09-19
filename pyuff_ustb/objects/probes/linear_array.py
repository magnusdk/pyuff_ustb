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


class LinearArray(Probe):
    """:class:`Uff` class to define a linear array probe geometry.

    :class:`LinearArray` defines an array of elements regularly place along a line.
    Optionally :class:`LinearArray` specifies element width and height, assuming the
    they are rectangular.

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

    # Optional properties
    @optional_property
    def element_width(self) -> float:
        "Width of the elements in the azimuth direction [m]"
        return LazyScalar(self._reader["element_width"])

    @optional_property
    def element_height(self) -> float:
        "Height of the elements in the elevation direction [m]"
        return LazyScalar(self._reader["element_height"])

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

        # Compute element abcissa
        x0 = np.arange(1, self.N + 1) * self.pitch
        x0 = x0 - np.mean(x0)

        return np.array(
            [
                x0,
                np.zeros(self.N),
                np.zeros(self.N),
                np.zeros(self.N),
                np.zeros(self.N),
                element_width * np.ones(self.N),
                element_height * np.ones(self.N),
            ]
        )
