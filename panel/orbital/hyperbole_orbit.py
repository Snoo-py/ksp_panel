from panel.orbital.orbit_plot import OrbitPlot
from panel.telemetry.telemetry import Telemetry
from panel.telemetry.hyperbole import HyperboleData



class HyperboleOrbit(OrbitPlot):

    def _update_points(self, telemetry):
        self.periapsis_plot.update_plot(telemetry)
        self.ascending_plot.update_plot(telemetry)
        self.descending_plot.update_plot(telemetry)
        self.ascending_descending.update_plot(telemetry)
        self.vessel_plot.update_plot(telemetry)


    def update_orbit(self, telemetry):
        telemetry.__class__ = HyperboleData
        self.remove()
        self._orbit_plot = self.axes.plot(telemetry.hyperbole_x, telemetry.hyperbole_y,
                                          color='green', linewidth=0.8)
        self._update_points(telemetry)
        telemetry.__class__ = Telemetry


    def remove(self):
        if self._orbit_plot:
            self._orbit_plot.pop(0).remove()
        OrbitPlot.remove(self)
        self._orbit_plot = None
