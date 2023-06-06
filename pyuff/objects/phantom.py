from pyuff.objects import PyuffObject
from pyuff.objects.base import compulsory_property, dependent_property
from pyuff.readers import LazyArray, LazyScalar


class Phantom(PyuffObject):
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
    def n_points(self):
        "Number of points"
        # TODO

    @dependent_property
    def x(self):
        "Points position in the x axis [m]"
        # TODO

    @dependent_property
    def y(self):
        "Points position in the y axis [m]"
        # TODO

    @dependent_property
    def z(self):
        "Points position in the z axis [m]"
        # TODO

    @dependent_property
    def hamma(self):
        "Reflection coefficient [unitless]"
        # TODO

    @dependent_property
    def r(self):
        "Distance from the points to the origin [m]"
        # TODO

    @dependent_property
    def theta(self):
        "Angle in the azimuth direction respect to origin [rad]"
        # TODO

    @dependent_property
    def phi(self):
        "Angle in the elevation direction respect to origin [rad]"
        # TODO
