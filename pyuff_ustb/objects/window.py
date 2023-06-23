from enum import Enum


class Window(Enum):
    """Enumeration for window types.

    :attr:`Window.boxcar`, :attr:`Window.rectangular` and :attr:`Window.flat` are
    semantically equivalent, even though they are different enumerations:

    >>> Window.boxcar == Window.rectangular == Window.flat
    True

    See also:
        :class:`~pyuff_ustb.objects.apodization.Apodization`

    Original authors:
        Alfonso Rodriguez-Molares (alfonso.r.molares@ntnu.no)
    """

    none = 0
    boxcar = 1
    rectangular = 1
    flat = 1
    hanning = 2
    hamming = 3
    tukey25 = 4
    tukey50 = 5
    tukey75 = 6
    tukey80 = 7
    sta = 7
    scanline = 8


if __name__ == "__main__":
    import doctest

    doctest.testmod()
