import numpy as np

from pyuff.objects.uff import Uff, compulsory_property
from pyuff.readers import LazyArray, util

# TODO: Redo me


class Apodization(Uff):
    @compulsory_property
    def probe(self):
        return util.read_probe(self._reader["probe"])

    @compulsory_property
    def focus(self):
        if "focus" in self._reader:
            return util.read_scan(self._reader["focus"])
        elif "scan" in self._reader:
            return util.read_scan(self._reader["scan"])
        return None

    @compulsory_property
    def sequence(self):
        from pyuff.objects.wave import Wave

        return util.read_potentially_list(self._reader["sequence"], Wave)

    @compulsory_property
    def window(self):
        from pyuff.objects.window import Window

        if "window" in self._reader:
            with self._reader["window"].h5_obj as h5_obj:
                return Window(np.squeeze(h5_obj[:]))
        return Window.none

    @compulsory_property
    def f_number(self):
        return LazyArray(self._reader["f_number"])

    # @compulsory_property
    # def M(self):
    #    return LazyArray(self._reader["M"])

    @compulsory_property
    def origin(self):
        from pyuff.objects.point import Point

        if "origin" in self._reader:
            return Point(self._reader["origin"])
        elif "origo" in self._reader:
            return Point(self._reader["origo"])

    @compulsory_property
    def tilt(self):
        return LazyArray(self._reader["tilt"])
