import numpy as np

from pyuff.objects.uff import Uff, compulsory_property, dependent_property
from pyuff.readers import LazyArray, LazyScalar


class Phantom(Uff):
    # Compulsory properties
    @compulsory_property
    def points(self):
        "Matrix of point scaterers [x y z Gamma] - [m m m unitless]"
        return LazyArray(self._reader["points"])

    @compulsory_property
    def time(self):
        "Time [s]"
        return LazyScalar(self._reader["time"])

    @compulsory_property
    def sound_speed(self):
        "Medium sound speed [m/s]"
        return LazyScalar(self._reader["sound_speed"])

    @compulsory_property
    def density(self):
        "Medium density [kg/m3]"
        return LazyScalar(self._reader["density"])

    @compulsory_property
    def alpha(self):
        "Medium attenuation [dB/cm/MHz]"
        return LazyScalar(self._reader["alpha"])

    # Dependent properties
    @dependent_property
    def N_points(self):
        "Number of points"
        return self.points.shape[0]

    @dependent_property
    def x(self):
        "Points position in the x axis [m]"
        return self.points[:, 0]

    @dependent_property
    def y(self):
        "Points position in the y axis [m]"
        return self.points[:, 1]

    @dependent_property
    def z(self):
        "Points position in the z axis [m]"
        return self.points[:, 2]

    @dependent_property
    def Gamma(self):
        "Reflection coefficient [unitless]"
        return self.points[:, 3]

    @dependent_property
    def r(self):
        "Distance from the points to the origin [m]"
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    @dependent_property
    def theta(self):
        "Angle in the azimuth direction respect to origin [rad]"
        return np.arctan2(self.x, self.z)

    @dependent_property
    def phi(self):
        "Angle in the elevation direction respect to origin [rad]"
        return np.arctan2(self.y, self.z)
