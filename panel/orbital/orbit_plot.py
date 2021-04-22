
from panel.telemetry.telemetry import Telemetry



class OrbitPlot(object):
    def __init__(self, compute_class=Telemetry, default_class=Telemetry):
        self._compute_class = compute_class
        self._default_class = default_class


    def update_orbit(self, telemetry):
        telemetry.__class__ = self._compute_class
        self.trajectory.update(telemetry)
        self.points.update(telemetry)
        telemetry.__class__ = self._default_class


    def remove(self):
        self.trajectory.remove()
        self.points.remove()
