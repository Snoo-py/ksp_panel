import numpy as np

from panel.planet_data import PLANET_DATA
from panel.telemetry.telemetry import Telemetry


class EllipseData(Telemetry):

    @property
    def _c(self):
        return (self.apoapsis - self.periapsis) / 2.0

    @property
    def focus_x(self):
        return self._c

    @property
    def focus_y(self):
        return 0

    @property
    def width(self):
        return 2 * self.semi_major_axis

    @property
    def height(self):
        return 2 * self.semi_minor_axis


    @property
    def proj_equ_width(self):
        x, y = self.projection(self.width, 0)
        return np.sqrt(x**2 + y**2)


    @property
    def proj_equ_height(self):
        x, y = self.projection(0, self.height)
        return np.sqrt(x**2 + y**2)
