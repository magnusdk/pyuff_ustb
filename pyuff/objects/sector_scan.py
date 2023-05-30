from functools import cached_property

from pyuff.objects.scan import Scan
from pyuff.readers import LazyArray


class SectorScan(Scan):
    @cached_property
    def azimuth_axis(self):
        return LazyArray(self._reader["azimuth_axis"])

    @cached_property
    def depth_axis(self):
        return LazyArray(self._reader["depth_axis"])

    @cached_property
    def origin(self):
        with self._reader.h5_obj as obj:
            if "origin" in obj:
                raise NotImplementedError()
            if "apex" in obj:
                from pyuff.objects.point import Point

                return Point(self._reader["apex"])
            return None
