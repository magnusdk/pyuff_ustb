import numpy as np

from pyuff.objects.scans.scan import Scan
from pyuff.objects.uff import compulsory_property, dependent_property
from pyuff.readers import LazyArray, util


class SectorScan(Scan):
    # Compulsory properties
    @compulsory_property
    def azimuth_axis(self):
        "Vector containing the azimuth coordinates [rad]"
        return LazyArray(self._reader["azimuth_axis"])

    @compulsory_property
    def depth_axis(self):
        "Vector containing the distance coordinates [m]"
        return LazyArray(self._reader["depth_axis"])

    @compulsory_property
    def origin(self):
        "Vector of UFF.POINT objects"
        from pyuff.objects.point import Point

        if "origin" in self._reader:
            return util.read_potentially_list(self._reader["origin"], Point)
        if "apex" in self._reader:
            return Point(self._reader["apex"])

    # Dependent properties
    @dependent_property
    def N_azimuth_axis(self):
        "Number of pixels in azimuth_axis"
        return len(self.azimuth_axis)

    @dependent_property
    def N_depth_axis(self):
        "Number of pixels in depth_axis"
        return len(self.depth_axis)

    @dependent_property
    def N_origins(self):
        "Number of scanline origins"
        if isinstance(self.origin, (list, tuple)):
            return len(self.origin)
        return 1

    @dependent_property
    def depth_step(self):
        "Step size along the depth axis [m]"
        return np.mean(np.diff(self.depth_axis))

    @dependent_property
    def reference_distance(self):
        "Distance used for the calculation of the phase term [m]"
        raise NotImplementedError("Create an issue on the repository if you need this.")

    # Unlike the base scan object (pyuff.Scan), x, y, and z are not compulsory
    # properties, but calculated based on azimuth_axis, depth_axis, and origin.
    @dependent_property
    def x(self):
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
    def y(self):
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
    def z(self):
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
