from panel.orbital.trajectory_plot import TrajectoryPlot



class TrajectoryHyperbole(TrajectoryPlot):

    def update(self, telemetry):
        self.remove()
        self._orbit_plot = self.axes.plot(telemetry.hyperbole_x, telemetry.hyperbole_y,
                                          color='green', linewidth=0.8)


    def remove(self):
        if self._orbit_plot:
            self._orbit_plot.pop(0).remove()
        self._orbit_plot = None
