from typing import TYPE_CHECKING, List, Union

import numpy as np

from pyuff_ustb.objects.scans.scan import Scan
from pyuff_ustb.objects.uff import compulsory_property, dependent_property
from pyuff_ustb.readers import LazyArray, util

if TYPE_CHECKING:
    from pyuff_ustb.objects.point import Point

    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class SectorScan(Scan):
    """:class:`Uff` class to define a sector scan.

    :class:`SectorScan` contains the position of the azimuth and depth axis from an
    origin. The origin may be a single point or a list of points with the same length
    as the ``azimuth_axis``. In the case of multiple origins, each origin represents the
    apex of a single azimuth direction/column of the scan.

    Original authors:
        * Alfonso Rodriguez-Molares <alfonso.r.molares@ntnu.no>
        * Anders E. Vrålstad <anders.e.vralstad@ntnu.no>
        * Stefano Fiorentini <stefano.fiorentini@ntnu.no>
    """

    # Compulsory properties
    @compulsory_property
    def azimuth_axis(self) -> np.ndarray:
        "Vector containing the azimuth coordinates [rad]"
        return LazyArray(self._reader["azimuth_axis"])

    @compulsory_property
    def depth_axis(self) -> np.ndarray:
        "Vector containing the distance coordinates [m]"
        return LazyArray(self._reader["depth_axis"])

    @compulsory_property
    def origin(self) -> Union["Point", List["Point"]]:
        "Vector of UFF.POINT objects"
        from pyuff_ustb.objects.point import Point

        if "origin" in self._reader:
            return util.read_potentially_list(self._reader["origin"], Point)
        if "apex" in self._reader:
            return Point(self._reader["apex"])

    # Dependent properties
    @dependent_property
    def N_azimuth_axis(self) -> int:
        "Number of pixels in azimuth_axis"
        return len(self.azimuth_axis)

    @dependent_property
    def N_depth_axis(self) -> int:
        "Number of pixels in depth_axis"
        return len(self.depth_axis)

    @dependent_property
    def N_origins(self) -> int:
        "Number of scanline origins"
        if isinstance(self.origin, (list, tuple)):
            return len(self.origin)
        return 1

    @dependent_property
    def depth_step(self) -> float:
        "Step size along the depth axis [m]"
        return np.mean(np.diff(self.depth_axis))

    @dependent_property
    def reference_distance(self):
        "Distance used for the calculation of the phase term [m]"
        raise NotImplementedError("Create an issue on the repository if you need this.")

    # Unlike the base scan object (pyuff_ustb.Scan), x, y, and z are not compulsory
    # properties, but calculated based on azimuth_axis, depth_axis, and origin.
    @dependent_property
    def x(self) -> np.ndarray:
        if (
            (self.azimuth_axis is None)
            or (self.depth_axis is None)
            or (self.origin is None)
        ):
            raise ValueError(
                "Cannot calculate x without azimuth_axis, depth_axis, and origin"
            )
        rho, theta = np.meshgrid(self.depth_axis, self.azimuth_axis, indexing="ij")
        N_pixels = rho.size
        return np.reshape(rho * np.sin(theta) + self.origin.x, [N_pixels])

    @dependent_property
    def y(self) -> np.ndarray:
        if (
            (self.azimuth_axis is None)
            or (self.depth_axis is None)
            or (self.origin is None)
        ):
            raise ValueError(
                "Cannot calculate y without azimuth_axis, depth_axis, and origin"
            )
        rho, theta = np.meshgrid(self.depth_axis, self.azimuth_axis, indexing="ij")
        N_pixels = rho.size
        return np.reshape(np.zeros(rho.shape) + self.origin.y, [N_pixels])

    @dependent_property
    def z(self) -> np.ndarray:
        if (
            (self.azimuth_axis is None)
            or (self.depth_axis is None)
            or (self.origin is None)
        ):
            raise ValueError(
                "Cannot calculate z without azimuth_axis, depth_axis, and origin"
            )
        rho, theta = np.meshgrid(self.depth_axis, self.azimuth_axis, indexing="ij")
        N_pixels = rho.size
        return np.reshape(rho * np.cos(theta) + self.origin.z, [N_pixels])
