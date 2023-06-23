from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.uff import (
    Uff,
    compulsory_property,
    dependent_property,
    optional_property,
)
from pyuff_ustb.readers import LazyScalar, util

if TYPE_CHECKING:
    from pyuff_ustb.objects.apodization import Apodization
    from pyuff_ustb.objects.point import Point
    from pyuff_ustb.objects.probes.probe import Probe
    from pyuff_ustb.objects.wavefront import Wavefront


class Wave(Uff):
    """:class:`Uff` class that describes a transmitted wave.

    :class:`Wave` contains information to describe a wave: ``planar``, ``spherical``, or ``photoacoustic``, and the apodization used to produce it.

    :attr:`wavefront` defines the type of wave produced: :attr:`Wavefront.plane`, :attr:`Wavefront.spherical`, or :attr:`Wavefront.photoacoustic`.

    :attr:`source` defines the wave attitude. If :attr:`wavefront` is :attr:`Wavefront.spherical` then :attr:`source` defines the point in space from which the wave originated. If :attr:`source` is behind the plane ``z=0`` then the spherical wave will be diverging. If :attr:`source` is in front of the plane ``z=0`` the the spherical wave will be converging. If the :attr:`wavefront` is :attr:`Wavefront.plane` then :attr:`source` defines the orientation through the azimuth and elevation angles, i.e. :attr:`source.distance` becomes meaningless. If the :attr:`wavefront` is :attr:`Wavefront.photoacoustic` then :attr:`source` is ignored.

    :attr:`Apodization` is a :class:`~pyuff_ustb.objects.apodization.Apodization` class used to compute the apodization values that generate the :class:`Wave`.

    :attr:`delay` defines the time interval between the reference time ``t0`` and the start of acquisition for this particular wave. We refer to reference time, or time zero, as the moment the wave passes through the origin of coordinates ``(0, 0, 0)``.

    See also:
        :class:`~pyuff_ustb.objects.wavefront.Wavefront`
        :class:`~pyuff_ustb.objects.apodization.Apodization`

    Original authors:
        * Alfonso Rodriguez-Molares <alfonso.r.molares@ntnu.no>
        * Ole Marius Hoel Rindal <olemarius@olemarius.net>
        * Anders E. Vrålstad <anders.e.vralstad@ntnu.no>
    """

    # Compulsory properties
    @compulsory_property
    def wavefront(self) -> "Wavefront":
        "WAVEFRONT enumeration class"
        from pyuff_ustb.objects.wavefront import Wavefront

        if "wavefront" in self._reader:
            return util.read_enum(self._reader["wavefront"], Wavefront)
        return Wavefront.spherical

    @compulsory_property
    def source(self) -> "Point":
        "POINT class"
        from pyuff_ustb.objects.point import Point

        return Point(self._reader["source"])

    @compulsory_property
    def origin(self) -> "Point":
        "POINT class"
        from pyuff_ustb.objects.point import Point

        return Point(self._reader["origin"])

    @compulsory_property
    def apodization(self) -> "Apodization":
        "APODIZATION class"
        from pyuff_ustb.objects.apodization import Apodization

        return Apodization(self._reader["apodization"])

    # Optional properties
    @optional_property
    def probe(self) -> "Probe":
        "PROBE class."
        return util.read_probe(self._reader["probe"])

    @optional_property
    def event(self) -> int:
        "Index of the transmit/receive event this wave refers to"
        return LazyScalar(self._reader["event"])

    @optional_property
    def delay(self) -> float:
        "Time interval between t0 and acquistion start [s]"
        if "delay" in self._reader:
            return LazyScalar(self._reader["delay"])
        return 0.0

    @optional_property
    def sound_speed(self) -> float:
        "Reference speed of sound [m/s]"
        if "sound_speed" in self._reader:
            return LazyScalar(self._reader["sound_speed"])
        return 1540.0

    # Dependent properties
    @dependent_property
    def N_elements(self) -> int:
        "Number of elements"
        return self.probe.N_elements

    @dependent_property
    def delay_values(self):
        "Delay [s]"
        raise NotImplementedError(
            "Delay value computation is outside the scope of pyuff_ustb"
        )

    @dependent_property
    def apodization_values(self):
        "Apodization [unitless]"
        raise NotImplementedError(
            "Apodization computation is outside the scope of pyuff_ustb"
        )
