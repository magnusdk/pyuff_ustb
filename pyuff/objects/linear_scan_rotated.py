from pyuff.objects.base import compulsory_property, dependent_property
from pyuff.objects.scan import Scan
from pyuff.readers import LazyArray, LazyScalar


class LinearScanRotated(Scan):
    # Compulsory properties
    @compulsory_property
    def x_axis(self):
        return LazyArray(self._reader["x_axis"])

    @compulsory_property
    def z_axis(self):
        return LazyArray(self._reader["z_axis"])

    @compulsory_property
    def rotation_angle(self):
        return LazyScalar(self._reader["rotation_angle"])

    @compulsory_property
    def center_of_rotation(self):
        return LazyArray(self._reader["center_of_rotation"])

    # Dependent properties
    @dependent_property
    def n_x_axis(self):
        "Number of pixels in the x_axis"
        # TODO

    @dependent_property
    def n_z_axis(self):
        "Number of pixels in the z_axis"
        # TODO

    @dependent_property
    def x_step(self):
        "The step size in m of the x samples"
        # TODO

    @dependent_property
    def z_step(self):
        "The step size in m of the z samples"
        # TODO

    @dependent_property
    def reference_distance(self):
        "Distance used for the calculation of the phase term"
        # TODO
