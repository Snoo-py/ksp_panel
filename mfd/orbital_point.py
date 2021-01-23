from matplotlib.lines import Line2D


class OrbitPointPlot(Line2D):
    def update_plot(self, x, y):
        self.set_xdata(self._list(x))
        self.set_ydata(self._list(y))

    def _list(self, value):
        if not isinstance(value, list):
            return [value]
        return value



class AscendingPlot(OrbitPointPlot):
    def __init__(self, x, y):
        # Plot ascending node position like a filled square
        Line2D.__init__(self, [x], [y], marker='s', markersize='6', color='green')



class DescendingPlot(OrbitPointPlot):
    def __init__(self, x, y):
        # Plot descending node position like a empy square
        Line2D.__init__(self, [x], [y], marker='s', markerfacecolor='black', markersize='6', color='green')



class AscendingDescendingLine(OrbitPointPlot):
    def __init__(self, xs, ys):
        # Plot dashed line between ascending and descending node
        Line2D.__init__(self, xs, ys, linestyle='--', marker='None', color='green')



class PeriapsisPlot(OrbitPointPlot):
    def __init__(self, x, y):
        # Plot periapsis position like a empty circle
        Line2D.__init__(self, [x], [y], marker='o', markerfacecolor='black', markersize='6', color='green')



class ApoapsisPlot(OrbitPointPlot):
    def __init__(self, x, y):
        # Plot apoapsis position like a filled circle
        Line2D.__init__(self, [x], [y], marker='o', markersize='6', color='green')



class VesselPlot(OrbitPointPlot):
    def __init__(self, x, y):
        # Plot vessel position like a line between the center of mass of the ref body and the vessel position
        Line2D.__init__(self, [0, x], [0, y], marker='None', color='green')


    def update_plot(self, x, y):
        self.set_xdata([0, x])
        self.set_ydata([0, y])
