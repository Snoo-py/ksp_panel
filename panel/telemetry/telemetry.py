import functools
import numpy as np
from enum import Enum

from panel.planet_data import PLANET_DATA




class PROJECTION(bytes, Enum):
    SHIP = (0, 'SHP')
    EQUATORIAL = (1, 'EQU')

    def __new__(cls, value, label):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.label = label
        return obj

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            index = 0
        return members[index]



def telemetry_cache(*checks):
    def inner_function(func):

        def init_cache(obj, key):
            if not '__cache_values' in obj.__dict__:
                obj.__dict__['__cache_values'] = {}
            if not key in obj.__dict__['__cache_values']:
                obj.__cache_values[key] = {
                    'current_value': None
                }

        def need_recalculate(obj, key, checks):
            need_recalculate = False
            for check in checks:
                if obj.__cache_values[key].get(check) != getattr(obj, check):
                    obj.__cache_values[key][check] = getattr(obj, check)
                    need_recalculate = True
            return need_recalculate

        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            key = func.__name__
            init_cache(self, key)
            if need_recalculate(self, key, checks):
                self.__cache_values[key]['current_value'] = func(self, *args, **kwargs)
            return self.__cache_values[key]['current_value']
        return wrap
    return inner_function



class Telemetry(object):
    def __init__(self):
        self.__dict__['_telemetry'] = {}
        self.projection_mode = PROJECTION.SHIP


    def __getattr__(self, name):
        if name in self._telemetry:
            return self._telemetry.get(name)
        return getattr(self, name)


    def __setattr__(self, name, value):
        if name in self.__dir__():
            object.__setattr__(self, name, value)
        else:
            self._telemetry[name] = value


    def str_km(self, param):
        """
        10 -> 10
        100 -> 100
        1,000 -> 1.000K
        10,000 -> 10.00K
        100,000 -> 100.0K
        1,000,000 -> 1.000M
        10,000,000 -> 10.00M
        100,000,000 -> 100.0M
        """
        value = self.__getattr__(param)
        i_value = float(value)
        n = 1
        unit = None
        if i_value < 0:
            n = -1
            i_value = -i_value

        if i_value < 1000.0:
            v = '%s' % (n * i_value)
        elif i_value < 1000000.0:
            v = '%s' % (n * i_value / 1000.0)
            unit = 'K'
        else:
            v = '%s' % (n * i_value / 1000000.0)
            unit = 'M'
        if unit:
            return '%s%s' % (v[:5], unit)
        return '%s' % v[:6]


    def projection(self, x, y):
        if self.projection_mode == PROJECTION.SHIP:
            return self.ship_projection(x, y)
        elif self.projection_mode == PROJECTION.EQUATORIAL:
            return self.equatorial_projection(x, y)
        return None


    def ship_projection(self, x, y):
        proj_1 = np.array([
            [self.cos_argument_of_periapsis, -self.sin_argument_of_periapsis],
            [self.sin_argument_of_periapsis,  self.cos_argument_of_periapsis]
        ])
        proj_2 = np.array([
            [self.cos_longitude_of_ascending_node, -self.sin_longitude_of_ascending_node],
            [self.sin_longitude_of_ascending_node,  self.cos_longitude_of_ascending_node]
        ])
        point = np.array([x, y])
        res = np.matmul(proj_1, point)
        res = np.matmul(proj_2, res)
        return res[0], res[1]


    def equatorial_projection(self, x, y):
        _x, _y = self.ship_projection(x, y)
        return _x * self.cos_inclination, _y


    def update_from_krpc_active_vessel(self, ut, active_vessel):
        orbit = active_vessel.orbit
        self.ut = ut
        self.update_from_krpc_orbit(orbit)
        self.time_to_ascending_node = orbit.ut_at_true_anomaly(-self.argument_of_periapsis) - self.ut
        self.time_to_descending_node = orbit.ut_at_true_anomaly(np.pi - self.argument_of_periapsis) - self.ut


    def update_from_krpc_orbit(self, orbit):
        self.apoapsis_altitude = orbit.apoapsis_altitude
        self.periapsis_altitude = orbit.periapsis_altitude
        self.eccentricity = orbit.eccentricity
        self.time_to_apoapsis = orbit.time_to_apoapsis
        self.time_to_periapsis = orbit.time_to_periapsis
        self.period = orbit.period
        self.inclination = orbit.inclination
        self.longitude_of_ascending_node = orbit.longitude_of_ascending_node
        self.argument_of_periapsis = orbit.argument_of_periapsis
        self.apoapsis = orbit.apoapsis
        self.periapsis = orbit.periapsis
        self.ref_body_name = orbit.body.name.lower()
        self.semi_major_axis = orbit.semi_major_axis
        self.semi_minor_axis = orbit.semi_minor_axis
        self.radius = orbit.radius
        self.orbital_speed = orbit.orbital_speed
        self.speed = orbit.speed
        self.true_anomaly = orbit.true_anomaly
        self.mean_anomaly = orbit.mean_anomaly


    @property
    def radius_altitude(self):
        return self.radius - PLANET_DATA[self.ref_body_name]['radius'] * 1000


    @property
    def periapsis_x(self):
        return self.periapsis


    @property
    def periapsis_y(self):
        return 0


    @property
    def apoapsis_x(self):
        if self.eccentricity < 1:
            return -self.apoapsis
        return None


    @property
    def apoapsis_y(self):
        if self.eccentricity < 1:
            return 0
        return None


    @property
    def longitude_of_periapsis_deg(self):
        return self.argument_of_periapsis_deg + self.longitude_of_ascending_node_deg


    @property
    def argument_of_periapsis_deg(self):
        return np.rad2deg(self.argument_of_periapsis)


    @property
    def longitude_of_ascending_node_deg(self):
        return np.rad2deg(self.longitude_of_ascending_node)


    @property
    def inclination_deg(self):
        return np.rad2deg(self.inclination)

    @property
    @telemetry_cache('inclination')
    def cos_inclination(self):
        return np.cos(self.inclination)

    @property
    def true_anomaly_deg(self):
        return np.rad2deg(self.true_anomaly)


    @property
    @telemetry_cache('longitude_of_ascending_node')
    def cos_longitude_of_ascending_node(self):
        return np.cos(self.longitude_of_ascending_node)


    @property
    @telemetry_cache('longitude_of_ascending_node')
    def sin_longitude_of_ascending_node(self):
        return np.sin(self.longitude_of_ascending_node)


    @property
    @telemetry_cache('argument_of_periapsis', 'longitude_of_ascending_node')
    def cos_longitude_of_periapsis(self):
        return np.cos(self.argument_of_periapsis + self.longitude_of_ascending_node)


    @property
    @telemetry_cache('argument_of_periapsis', 'longitude_of_ascending_node')
    def sin_longitude_of_periapsis(self):
        return np.sin(self.argument_of_periapsis + self.longitude_of_ascending_node)


    @property
    @telemetry_cache('argument_of_periapsis')
    def cos_argument_of_periapsis(self):
        return np.cos(self.argument_of_periapsis)


    @property
    @telemetry_cache('argument_of_periapsis')
    def sin_argument_of_periapsis(self):
        return np.sin(self.argument_of_periapsis)


    @property
    def vessel_x(self):
        return self.radius * np.cos(self.true_anomaly)


    @property
    def vessel_y(self):
        return self.radius * np.sin(self.true_anomaly)


    @property
    def _p(self):
        return self.semi_minor_axis**2 / self.semi_major_axis


    @property
    def ascending_node_radius(self):
        return self._p / (1 + self.eccentricity * self.cos_argument_of_periapsis)


    @property
    def descending_node_radius(self):
        return self._p / (1 - self.eccentricity * self.cos_argument_of_periapsis)


    @property
    def ascending_node_x(self):
        return self.ascending_node_radius * self.cos_argument_of_periapsis


    @property
    def ascending_node_y(self):
        return -self.ascending_node_radius * self.sin_argument_of_periapsis


    @property
    def descending_node_x(self):
        return -self.descending_node_radius * self.cos_argument_of_periapsis # cos(x+pi)=-cos(x)


    @property
    def descending_node_y(self):
        return self.descending_node_radius * self.sin_argument_of_periapsis # sin(x+pi)=-sin(x)
