from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.scans.scan import Scan
from pyuff_ustb.objects.uff import compulsory_property, dependent_property
from pyuff_ustb.readers import LazyArray, LazyScalar

if TYPE_CHECKING:
    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class LinearScanRotated(Scan):
    """:class:`Uff` class to define a rotated linear scan."""

    # Compulsory properties
    @compulsory_property
    def x_axis(self) -> np.ndarray:
        "Vector containing the x coordinates of the x - axis [m]"
        return LazyArray(self._reader["x_axis"])

    @compulsory_property
    def z_axis(self) -> np.ndarray:
        "Vector containing the z coordinates of the z - axis [m]"
        return LazyArray(self._reader["z_axis"])

    @compulsory_property
    def rotation_angle(self) -> float:
        "Rotation angle [rad]"
        return LazyScalar(self._reader["rotation_angle"])

    @compulsory_property
    def center_of_rotation(self) -> np.ndarray:
        "Vector containing the (x,y,z) coordinates [m] of the rotation point"
        return LazyArray(self._reader["center_of_rotation"])

    # Dependent properties
    @dependent_property
    def N_x_axis(self) -> int:
        "Number of pixels in the x_axis"
        return len(self.x_axis)

    @dependent_property
    def N_z_axis(self) -> int:
        "Number of pixels in the z_axis"
        return len(self.z_axis)

    @dependent_property
    def x_step(self) -> float:
        "The step size in m of the x samples"
        return np.mean(np.diff(self.x_axis))

    @dependent_property
    def z_step(self) -> float:
        "The step size in m of the z samples"
        return np.mean(np.diff(self.z_axis))

    @dependent_property
    def reference_distance(self) -> np.ndarray:
        "Distance used for the calculation of the phase term"
        return self.z
