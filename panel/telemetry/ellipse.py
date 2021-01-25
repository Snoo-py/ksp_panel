import numpy as np

from panel.planet_data import PLANET_DATA
from panel.telemetry.telemetry import Telemetry



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
