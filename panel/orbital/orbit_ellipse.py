
from panel.orbital.orbit_plot import OrbitPlot
from panel.orbital.orbital_points_plot import OrbitalPointsPlot
from panel.orbital.trajectory_ellipse import TrajectoryEllipse
from panel.telemetry.ellipse import EllipseData


class OrbitalPointsEllipse(OrbitalPointsPlot):
    def update(self, telemetry):
        self.periapsis_plot.update_plot(telemetry)
        self.apoapsis_plot.update_plot(telemetry)
        self.ascending_plot.update_plot(telemetry)
        self.descending_plot.update_plot(telemetry)
        self.ascending_descending.update_plot(telemetry)
        self.vessel_plot.update_plot(telemetry)



class OrbitEllipse(OrbitPlot):
    def __init__(self, axes):
        OrbitPlot.__init__(self, compute_class=EllipseData)
        self.trajectory = TrajectoryEllipse(axes)
        self.points = OrbitalPointsEllipse(axes)

