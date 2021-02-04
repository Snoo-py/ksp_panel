from matplotlib.lines import Line2D


class OrbitPointPlot(object):
    def __init__(self, axes, *args, **kwargs):
        self._axes = axes
        self._args = args
        self._kwargs = kwargs
        self._plot = None


    def _create_plot(self, telemetry):
        x, y = telemetry.projection(self._get_x(telemetry), self._get_y(telemetry))
        self._plot = Line2D(x, y, *self._args, **self._kwargs)
        self._axes.add_line(self._plot)


    def update_plot(self, telemetry):
        if not self._plot:
            self._create_plot(telemetry)
        else:
            x, y = telemetry.projection(self._get_x(telemetry), self._get_y(telemetry))
            self._plot.set_xdata(x)
            self._plot.set_ydata(y)


    def _get_x(self, telemetry):
        """
        Return list with x from corresponding data in telemetry
        """
        pass


    def _get_y(self, telemetry):
        """
        Return list with y from corresponding data in telemetry
        """
        pass


    def remove(self):
        if self._plot:
            self._plot.remove()
            self._plot = None



class AscendingPlot(OrbitPointPlot):
    def __init__(self, axes):
        # Plot ascending node position like a filled square
        OrbitPointPlot.__init__(self, axes, marker='s', markersize='6', color='green')


    def _get_x(self, telemetry):
        return [telemetry.ascending_node_x]


    def _get_y(self, telemetry):
         return [telemetry.ascending_node_y]



class DescendingPlot(OrbitPointPlot):
    def __init__(self, axes):
        # Plot descending node position like a empy square
        OrbitPointPlot.__init__(self, axes, marker='s', markerfacecolor='black', markersize='6', color='green')


    def _get_x(self, telemetry):
        return [telemetry.descending_node_x]


    def _get_y(self, telemetry):
         return [telemetry.descending_node_y]



class AscendingDescendingLine(OrbitPointPlot):
    def __init__(self, axes):
        # Plot dashed line between ascending and descending node
        OrbitPointPlot.__init__(self, axes, linestyle='--', marker='None', color='green')


    def _get_x(self, telemetry):
        return [telemetry.ascending_node_x, telemetry.descending_node_x]


    def _get_y(self, telemetry):
         return [telemetry.ascending_node_y, telemetry.descending_node_y]



class PeriapsisPlot(OrbitPointPlot):
    def __init__(self, axes):
        # Plot periapsis position like a empty circle
        OrbitPointPlot.__init__(self, axes, marker='o', markerfacecolor='black', markersize='6', color='green')


    def _get_x(self, telemetry):
        return [telemetry.periapsis_x]


    def _get_y(self, telemetry):
         return [telemetry.periapsis_y]



class ApoapsisPlot(OrbitPointPlot):
    def __init__(self, axes):
        # Plot apoapsis position like a filled circle
        OrbitPointPlot.__init__(self, axes, marker='o', markersize='6', color='green')


    def _get_x(self, telemetry):
        return [telemetry.apoapsis_x]


    def _get_y(self, telemetry):
         return [telemetry.apoapsis_y]



class VesselPlot(OrbitPointPlot):
    def __init__(self, telemetry):
        # Plot vessel position like a line between the center of mass of the ref body and the vessel position
        OrbitPointPlot.__init__(self, telemetry, marker='None', color='green')


    def _get_x(self, telemetry):
        return [0, telemetry.vessel_x]


    def _get_y(self, telemetry):
         return [0, telemetry.vessel_y]