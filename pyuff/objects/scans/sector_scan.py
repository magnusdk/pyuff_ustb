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
