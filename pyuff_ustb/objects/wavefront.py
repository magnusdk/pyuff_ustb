from enum import Enum


class Wavefront(Enum):
    """Enumeration for wave types.

    See also:
        :class:`~pyuff_ustb.objects.wave.Wave`

    Original authors:
        Alfonso Rodriguez-Molares (alfonso.r.molares@ntnu.no)
    """

    plane = 0
    spherical = 1
    photoacoustic = 2
