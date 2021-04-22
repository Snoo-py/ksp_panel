
from panel.orbital.orbit_plot import OrbitPlot
from panel.orbital.orbital_points_plot import OrbitalPointsPlot
from panel.orbital.trajectory_hyperbole import TrajectoryHyperbole
from panel.telemetry.hyperbole import HyperboleData


class OrbitalPointsHyperbole(OrbitalPointsPlot):
    def update(self, telemetry):
        self.periapsis_plot.update_plot(telemetry)
        self.ascending_plot.update_plot(telemetry)
        self.descending_plot.update_plot(telemetry)
        self.ascending_descending.update_plot(telemetry)
        self.vessel_plot.update_plot(telemetry)



class OrbitHyperbole(OrbitPlot):
    def __init__(self, axes):
        OrbitPlot.__init__(self, compute_class=HyperboleData)
        self.trajectory = TrajectoryHyperbole(axes)
        self.points = OrbitalPointsHyperbole(axes)
