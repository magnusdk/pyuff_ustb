import numpy as np

from pyuff.objects.uff import (
    Uff,
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff.readers import LazyArray, util


class Apodization(Uff):
    # Compulsory properties
    @compulsory_property
    def probe(self):
        "UFF.PROBE class (needed for transmit & receive apodization)"
        return util.read_probe(self._reader["probe"])

    @compulsory_property
    def focus(self):
        "UFF.SCAN class (needed for transmit, receive & synthetic apodization)"
        if "focus" in self._reader:
            return util.read_scan(self._reader["focus"])
        elif "scan" in self._reader:
            return util.read_scan(self._reader["scan"])
        return None

    @compulsory_property
    def sequence(self):
        "Collection of UFF.WAVE classes (needed for synthetic apodizaton)"
        from pyuff.objects.wave import Wave

        return util.read_potentially_list(self._reader["sequence"], Wave)

    @compulsory_property
    def f_number(self):
        "F-number [Fx Fy] [unitless unitless]"
        # TODO: Default value = [1, 1]
        return LazyArray(self._reader["f_number"])

    @compulsory_property
    def window(self):
        "UFF.WINDOW class, default uff.window.none"
        from pyuff.objects.window import Window

        if "window" in self._reader:
            with self._reader["window"].h5_obj as h5_obj:
                return Window(np.squeeze(h5_obj[:]))
        return Window.none

    @compulsory_property
    def MLA(self):
        "Number of multi-line acquisitions, only valid for uff.window.scanline"
        # TODO: Default value = 1
        return LazyArray(self._reader["MLA"])

    @compulsory_property
    def MLA_overlap(self):
        "Number of multi-line acquisitions, only valid for uff.window.scanline"
        # TODO: Default value = 0
        return LazyArray(self._reader["MLA_overlap"])

    @compulsory_property
    def tilt(self):
        "Tilt angle [azimuth elevation] [rad rad]"
        # TODO: Default value = [0, 0]
        return LazyArray(self._reader["tilt"])

    @compulsory_property
    def minimum_aperture(self):
        "Minimum aperture size in the [x y] direction"
        # TODO: Default value = [1e-3, 1e-3]
        return LazyArray(self._reader["minimum_aperture"])

    @compulsory_property
    def maximum_aperture(self):
        "Maximum aperture size in the [x y] direction"
        # TODO: Default value = [10, 10]
        return LazyArray(self._reader["maximum_aperture"])

    # Optional properties
    @optional_property
    def apodization_vector(self):
        "Apodization vector to override the dynamic calculation of apodization"
        return LazyArray(self._reader["apodization_vector"])

    @optional_property
    def origin(self):
        """POINT class to overwrite the location of the aperture window as computed on
        the wave source location"""
        from pyuff.objects.point import Point

        if "origin" in self._reader:
            return Point(self._reader["origin"])
        elif "origo" in self._reader:
            return Point(self._reader["origo"])
        elif "apex" in self._reader:
            return Point(self._reader["apex"])
        return None

    # Dependent properties
    @dependent_property
    def data(self):
        "Apodization data"
        raise NotImplementedError(
            "Apodization computation is outside the scope of pyuff"
        )

    @dependent_property
    def N_elements(self):
        "Number of elements (real or synthetic)"
        if len(self.sequence) == 0:
            assert self.probe is not None, "The PROBE parameter is not set."
            return self.probe.N_elements
        else:
            return len(self.sequence)
