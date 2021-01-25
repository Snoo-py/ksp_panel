from matplotlib.patches import Ellipse

from panel.orbital.orbit_plot import OrbitPlot
from panel.telemetry.telemetry import Telemetry
from panel.telemetry.ellipse import EllipseData



class EllipseOrbit(OrbitPlot):

    def _create_orbit(self, telemetry):
        angle = telemetry.argument_of_periapsis_deg + telemetry.longitude_of_ascending_node_deg
        self._orbit_plot = Ellipse((-telemetry.focus_x, -telemetry.focus_y),
                                      width=telemetry.width, height=telemetry.height,
                                      angle=angle, fill=False, color='green')
        self._axes.add_patch(self._orbit_plot)


    def _update_points(self, telemetry):
        self.periapsis_plot.update_plot(telemetry)
        self.apoapsis_plot.update_plot(telemetry)
        self.ascending_plot.update_plot(telemetry)
        self.descending_plot.update_plot(telemetry)
        self.ascending_descending.update_plot(telemetry)
        self.vessel_plot.update_plot(telemetry)


    def update_orbit(self, telemetry):
        telemetry.__class__ = EllipseData
        if not self._orbit_plot:
            self._create_orbit(telemetry)
        else:
            angle = telemetry.argument_of_periapsis_deg + telemetry.longitude_of_ascending_node_deg
            self._orbit_plot.center = (-telemetry.focus_x, -telemetry.focus_y)
            self._orbit_plot.width = telemetry.width
            self._orbit_plot.height = telemetry.height
            self._orbit_plot.angle = angle
        self._update_points(telemetry)
        telemetry.__class__ = Telemetry


    def remove(self):
        if self._orbit_plot:
            self._orbit_plot.remove()
        self._orbit_plot = None
        OrbitPlot.remove(self)
