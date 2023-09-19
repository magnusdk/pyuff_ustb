from typing import TYPE_CHECKING

import numpy as np

from pyuff_ustb.objects.uff import Uff, compulsory_property, dependent_property
from pyuff_ustb.readers import LazyArray

if TYPE_CHECKING:
    from pyuff_ustb.objects.point import Point

    # Make sure properties are treated as properties when type checking
    compulsory_property = property
    optional_property = property
    dependent_property = property


class Probe(Uff):
    """:class:`Uff` class to define arbitrary probe geometries.

    :class:`Probe` contains the position and attitude of all elements of a probe.
    Optionally :class:`Probe` can hold each element width and height, assuming the
    elements were rectangular. Information is stored in a single matrix form called
    geometry, one row per element containing:
    ``[x, y, z, azimuth, elevation, width, height]``.

    Original authors:
        Alfonso Rodriguez-Molares (alfonsom@ntnu.no)
    """

    # Compulsory properties
    @compulsory_property
    def geometry(self) -> np.ndarray:
        """An array with attitude of rectangular elements.

        The returned array contains 7 fields (over all elements):

        - x [meters]
        - y [meters]
        - z [meters]
        - theta [radians]
        - phi [radians]
        - width [meters]
        - height [meters]


        Returns:
            np.ndarray: An array with attitude of rectangular elements with shape
            ``(7, n_elements)``.
        """
        return LazyArray(self._reader["geometry"])

    @compulsory_property
    def origin(self) -> "Point":
        "Location of the probe respect to origin of coordinates"
        from pyuff_ustb.objects.point import Point

        return Point(self._reader["origin"])

    # Dependent properties
    @dependent_property
    def N_elements(self) -> int:
        "Number of elements"
        return self.geometry.shape[1]

    @dependent_property
    def x(self) -> np.ndarray:
        "Center of the element in the x axis [m]"
        return self.geometry[0]

    @dependent_property
    def y(self) -> np.ndarray:
        "Center of the element in the y axis [m]"
        return self.geometry[1]

    @dependent_property
    def z(self) -> np.ndarray:
        "Center of the element in the z axis [m]"
        return self.geometry[2]

    @dependent_property
    def xyz(self) -> np.ndarray:
        "Center of the element as an array of shape (n_elements, 3) [m]"
        return np.stack([self.x, self.y, self.z], -1)

    @dependent_property
    def theta(self) -> np.ndarray:
        "Orientation of the element in the azimuth direction [rad]"
        return self.geometry[3]

    @dependent_property
    def phi(self) -> np.ndarray:
        "Orientation of the element in the elevation direction [rad]"
        return self.geometry[4]

    @dependent_property
    def width(self) -> np.ndarray:
        "Element width [m]"
        return self.geometry[5]

    @dependent_property
    def height(self) -> np.ndarray:
        "Element height [m]"
        return self.geometry[6]

    @dependent_property
    def r(self) -> np.ndarray:
        "Distance from the element center to the origin of coordinates [m]"
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
