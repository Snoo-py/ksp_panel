import numpy as np

from planet_data import PLANET_DATA
from telemetry import Telemetry, telemetry_cache



class EllipseData(Telemetry):

    @property
    def _c(self):
        return (self.apoapsis - self.periapsis) / 2.0

    @property
    def focus_x(self):
        return self._c * self.cos_longitude_of_periapsis

    @property
    def focus_y(self):
        return self._c * self.sin_longitude_of_periapsis

    @property
    def width(self):
        return 2 * self.semi_major_axis

    @property
    def height(self):
        return 2 * self.semi_minor_axis



class HyperboleData(Telemetry):

    @property
    def _c3(self):
        # https://en.wikipedia.org/wiki/Hyperbolic_trajectory
        return self.speed**2 - 2 * PLANET_DATA[self.ref_body_name.lower()]['mu'] * 10**9 / self.radius


    @property
    def _a(self):
        # https://en.wikipedia.org/wiki/Characteristic_energy
        return -PLANET_DATA[self.ref_body_name.lower()]['mu'] * 10**9 / self._c3


    @property
    def _l(self):
        # https://en.wikipedia.org/wiki/Characteristic_energy
        return self._a * (1 - self.eccentricity**2)


    @property
    @telemetry_cache('eccentricity', '_l')
    def _limit_soi(self):
        return np.arccos((self._l / (PLANET_DATA[self.ref_body_name.lower()]['soi']*1000*3) - 1) / self.eccentricity)


    @property
    @telemetry_cache('eccentricity')
    def _limit_asymp(self):
        return np.arccos(-1 / self.eccentricity)


    @property
    def _limit(self):
        if self._limit_soi < self._limit_asymp:
            return self._limit_soi
        return self._limit_asymp


    @property
    @telemetry_cache('_limit')
    def _t(self):
        return np.linspace(-self._limit, self._limit, num=100)


    @property
    @telemetry_cache('eccentricity', '_l', '_t')
    def _r(self):
        # https://en.wikipedia.org/wiki/Characteristic_energy
        return  self._l / (1 + self.eccentricity * np.cos(self._t))


    @property
    @telemetry_cache('_r', '_t')
    def _xx(self):
        return self._r * np.cos(self._t)


    @property
    @telemetry_cache('_r', '_t')
    def _yy(self):
        return self._r * np.sin(self._t)


    @property
    def hyperbole_x(self):
        return  self._xx * self.cos_longitude_of_periapsis - self._yy * self.sin_longitude_of_periapsis


    @property
    def hyperbole_y(self):
        return self._xx * self.sin_longitude_of_periapsis + self._yy * self.cos_longitude_of_periapsis