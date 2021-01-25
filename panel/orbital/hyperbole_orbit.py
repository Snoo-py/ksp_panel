from panel.orbital.orbit_plot import OrbitPlot
from panel.telemetry.telemetry import Telemetry
from panel.telemetry.hyperbole import HyperboleData



class HyperboleOrbit(OrbitPlot):

    def update_orbit(self, telemetry):
        telemetry.__class__ = HyperboleData
        self.remove()
        self._orbit_plot = self.axes.plot(telemetry.hyperbole_x, telemetry.hyperbole_y,
                                          color='green', linewidth=0.8)
        telemetry.__class__ = Telemetry


    def remove(self):
        if self._orbit_plot:
            self._orbit_plot.pop(0).remove()
        self._orbit_plot = None
