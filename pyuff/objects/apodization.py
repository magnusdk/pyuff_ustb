import numpy as np

from pyuff.objects.base import PyuffObject, compulsory_property
from pyuff.readers import LazyArray, util

# TODO: Redo me


class Apodization(PyuffObject):
    @compulsory_property
    def probe(self):
        if "probe" in self._reader:
            return util.read_probe(self._reader["probe"])

    @compulsory_property
    def focus(self):
        with self._reader.h5_obj as h5_obj:
            if "focus" in h5_obj:
                focus_reader = self._reader["focus"]
            elif "scan" in h5_obj:
                focus_reader = self._reader["scan"]
            else:
                return None
        return util.read_scan(focus_reader)

    @compulsory_property
    def sequence(self):
        if "sequence" in self._reader:
            return util.read_sequence(self._reader["sequence"])

    @compulsory_property
    def window(self):
        from pyuff.objects.window import Window

        with self._reader.h5_obj as h5_obj:
            return Window(np.squeeze(h5_obj["window"][:]))

    @compulsory_property
    def f_number(self):
        return LazyArray(self._reader["f_number"])

    # @compulsory_property
    # def M(self):
    #    return LazyArray(self._reader["M"])

    @compulsory_property
    def origin(self):
        from pyuff.objects.point import Point

        with self._reader.h5_obj as h5_obj:
            if "origin" in h5_obj:
                return Point(self._reader["origin"])
            elif "origo" in h5_obj:
                return Point(self._reader["origo"])

    @compulsory_property
    def tilt(self):
        return LazyArray(self._reader["tilt"])
