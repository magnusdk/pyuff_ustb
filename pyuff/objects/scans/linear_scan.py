import numpy as np

from pyuff.objects.scans.scan import Scan
from pyuff.objects.uff import compulsory_property, dependent_property
from pyuff.readers import LazyArray


class LinearScan(Scan):
    # Compulsory properties
    @compulsory_property
    def x_axis(self):
        "Vector containing the x coordinates of the x-axis [m]"
        return LazyArray(self._reader["x_axis"])

    @compulsory_property
    def z_axis(self):
        "Vector containing the z coordinates of the z-axis [m]"
        return LazyArray(self._reader["z_axis"])

    # Dependent properties
    @dependent_property
    def N_x_axis(self):
        "Number of pixels in the x_axis"
        return len(self.x_axis)

    @dependent_property
    def N_z_axis(self):
        "Number of pixels in the z_axis"
        return len(self.z_axis)

    @dependent_property
    def x_step(self):
        "The step size in m of the x samples"
        return np.mean(np.diff(self.x_axis))

    @dependent_property
    def z_step(self):
        "The step size in m of the z samples"
        return np.mean(np.diff(self.z_axis))

    @dependent_property
    def reference_distance(self):
        "Distance used for the calculation of the phase term"
        return self.z
