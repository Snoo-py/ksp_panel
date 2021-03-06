import numpy as np

from panel.planet_data import PLANET_DATA
from panel.telemetry.telemetry import Telemetry, telemetry_cache



class HyperboleData(Telemetry):

    @property
    def _c3(self):
        # https://en.wikipedia.org/wiki/Hyperbolic_trajectory
        return self.speed**2 - 2 * PLANET_DATA[self.ref_body_name]['mu'] * 10**9 / self.radius


    @property
    def _a(self):
        # https://en.wikipedia.org/wiki/Characteristic_energy
        return -PLANET_DATA[self.ref_body_name]['mu'] * 10**9 / self._c3


    @property
    def _l(self):
        # https://en.wikipedia.org/wiki/Characteristic_energy
        return self._a * (1 - self.eccentricity**2)


    @property
    def _p(self):
        return self._l


    @property
    @telemetry_cache('eccentricity', '_l')
    def _limit_soi(self):
        return np.arccos((self._l / (PLANET_DATA[self.ref_body_name]['soi']*1000*3) - 1) / self.eccentricity)


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
