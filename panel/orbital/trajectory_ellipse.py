
import numpy as np
from matplotlib.patches import Ellipse
from panel.orbital.trajectory_plot import TrajectoryPlot



class TrajectoryEllipse(TrajectoryPlot):

    def _create_trajectory(self, telemetry):
        x, y = telemetry.projection(-telemetry.focus_x, -telemetry.focus_y)
        x_w, y_w = telemetry.projection(telemetry.width, 0)
        width = np.sqrt(x_w**2 + y_w**2)
        x_h, y_h = telemetry.projection(0, telemetry.height)
        height = np.sqrt(x_h**2 + y_h**2)
        self._orbit_plot = Ellipse((x, y),
                                   width=width, height=height,
                                   angle=telemetry.longitude_of_ascending_node_deg + telemetry.argument_of_periapsis_deg,
                                   fill=False, color='green')
        self._axes.add_patch(self._orbit_plot)


    def update(self, telemetry):
        if not self._orbit_plot:
            self._create_trajectory(telemetry)
        else:
            x, y = telemetry.projection(-telemetry.focus_x, -telemetry.focus_y)
            x_w, y_w = telemetry.projection(telemetry.width, 0)
            width = np.sqrt(x_w**2 + y_w**2)
            x_h, y_h = telemetry.projection(0, telemetry.height)
            height = np.sqrt(x_h**2 + y_h**2)
            self._orbit_plot.center = (x, y)
            self._orbit_plot.width = width
            self._orbit_plot.height = height
            self._orbit_plot.angle = telemetry.longitude_of_ascending_node_deg + telemetry.argument_of_periapsis_deg


    def remove(self):
        if self._orbit_plot:
            self._orbit_plot.remove()
        self._orbit_plot = None
