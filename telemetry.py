import functools
import numpy as np

from planet_data import PLANET_DATA


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


    def __getattr__(self, name):
        return self._telemetry.get(name)


    def __setattr__(self, name, value):
        if name in self.__dir__():
            object.__setattr__(self, name, value)
        else:
            self._telemetry[name] = value


    @property
    def radius_altitude(self):
        return self.radius - PLANET_DATA[self.ref_body_name]['radius'] * 1000


    @property
    def periapsis_x(self):
        return self.periapsis * self.cos_longitude_of_periapsis


    @property
    def periapsis_y(self):
        return self.periapsis * self.sin_longitude_of_periapsis

    @property
    def apoapsis_x(self):
        if self.eccentricity < 1:
            return -self.apoapsis * self.cos_longitude_of_periapsis
        return None

    @property
    def apoapsis_y(self):
        if self.eccentricity < 1:
            return -self.apoapsis * self.sin_longitude_of_periapsis
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
    def vessel_x(self):
        return self.radius * np.cos(self.true_anomaly + self.argument_of_periapsis + self.longitude_of_ascending_node)


    @property
    def vessel_y(self):
        return self.radius * np.sin(self.true_anomaly + self.argument_of_periapsis + self.longitude_of_ascending_node)


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
        return self.ascending_node_radius * self.cos_longitude_of_ascending_node


    @property
    def ascending_node_y(self):
        return self.ascending_node_radius * self.sin_longitude_of_ascending_node


    @property
    def descending_node_x(self):
        return -self.descending_node_radius * self.cos_longitude_of_ascending_node # cos(x+pi)=-cos(x)


    @property
    def descending_node_y(self):
        return -self.descending_node_radius * self.sin_longitude_of_ascending_node # sin(x+pi)=-sin(x)
