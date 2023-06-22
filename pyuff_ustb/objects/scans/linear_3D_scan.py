from pyuff_ustb.objects.scans.scan import Scan
from pyuff_ustb.objects.uff import compulsory_property, optional_property
from pyuff_ustb.readers import LazyArray, LazyScalar


class Linear3DScan(Scan):
    # Compulsory properties
    @compulsory_property
    def radial_axis(self) -> float:
        "Vector containing the coordinates in the radial direction axis [m]"
        return LazyArray(self._reader["radial_axis"])

    @compulsory_property
    def axial_axis(self) -> float:
        "Vector containing the coordinates in the axial direction axis [m]"
        return LazyArray(self._reader["axial_axis"])

    @compulsory_property
    def roll(self) -> float:
        "Angle between the radial axis and the x-axis [rad]"
        return LazyScalar(self._reader["roll"])

    # Optional properties
    @optional_property
    def n_radial_axis(self) -> int:
        "Number of pixels in the x_axis"
        return len(self.radial_axis)

    @optional_property
    def n_axial_axis(self) -> int:
        "Number of pixels in the z_axis"
        return len(self.axial_axis)
