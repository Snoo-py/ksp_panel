from panel.orbital.orbital_point import PeriapsisPlot, ApoapsisPlot, AscendingPlot, DescendingPlot, AscendingDescendingLine, VesselPlot


class OrbitPlot(object):
    def __init__(self, axes):
        self._axes = axes
        self._orbit_plot = None
        self.periapsis_plot = PeriapsisPlot(axes)
        self.apoapsis_plot = ApoapsisPlot(axes)
        self.ascending_plot = AscendingPlot(axes)
        self.descending_plot = DescendingPlot(axes)
        self.ascending_descending = AscendingDescendingLine(axes)
        self.vessel_plot = VesselPlot(axes)


    def update_orbit(self, telemetry):
        pass


    def remove(self):
        self.periapsis_plot.remove()
        self.apoapsis_plot.remove()
        self.ascending_plot.remove()
        self.descending_plot.remove()
        self.ascending_descending.remove()
        self.vessel_plot.remove()