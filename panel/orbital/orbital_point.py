from matplotlib.lines import Line2D


class OrbitPointPlot(Line2D):
    def __init__(self, telemetry, *args, **kwargs):
        Line2D.__init__(self, self._get_x(telemetry), self._get_y(telemetry), *args, **kwargs)


    def update_plot(self, telemetry):
        self.set_xdata(self._get_x(telemetry))
        self.set_ydata(self._get_y(telemetry))


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




class AscendingPlot(OrbitPointPlot):
    def __init__(self, telemetry):
        # Plot ascending node position like a filled square
        OrbitPointPlot.__init__(self, telemetry, marker='s', markersize='6', color='green')


    def _get_x(self, telemetry):
        return [telemetry.ascending_node_x]


    def _get_y(self, telemetry):
         return [telemetry.ascending_node_y]



class DescendingPlot(OrbitPointPlot):
    def __init__(self, telemetry):
        # Plot descending node position like a empy square
        OrbitPointPlot.__init__(self, telemetry, marker='s', markerfacecolor='black', markersize='6', color='green')


    def _get_x(self, telemetry):
        return [telemetry.descending_node_x]


    def _get_y(self, telemetry):
         return [telemetry.descending_node_y]



class AscendingDescendingLine(OrbitPointPlot):
    def __init__(self, telemetry):
        # Plot dashed line between ascending and descending node
        OrbitPointPlot.__init__(self, telemetry, linestyle='--', marker='None', color='green')


    def _get_x(self, telemetry):
        return [telemetry.ascending_node_x, telemetry.descending_node_x]


    def _get_y(self, telemetry):
         return [telemetry.ascending_node_y, telemetry.descending_node_y]



class PeriapsisPlot(OrbitPointPlot):
    def __init__(self, telemetry):
        # Plot periapsis position like a empty circle
        OrbitPointPlot.__init__(self, telemetry, marker='o', markerfacecolor='black', markersize='6', color='green')


    def _get_x(self, telemetry):
        return [telemetry.periapsis_x]


    def _get_y(self, telemetry):
         return [telemetry.periapsis_y]



class ApoapsisPlot(OrbitPointPlot):
    def __init__(self, telemetry):
        # Plot apoapsis position like a filled circle
        OrbitPointPlot.__init__(self, telemetry, marker='o', markersize='6', color='green')


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