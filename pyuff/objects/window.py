"""An enumeration of window types.

Tests:
>>> window.boxcar == window.rectangular == window.flat
True
>>> window(0)
<window.none: 0>
>>> window(8)
<window.scanline: 8>
"""


from enum import Enum


class window(Enum):
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
