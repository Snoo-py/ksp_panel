from matplotlib.patches import Ellipse

from panel.planet_data import PLANET_DATA



class RefPlanetPlot(object):
    def __init__(self, axes):
        self._axes = axes
        self._ref_planet_name = None
        self._ref_planet_plot = None
        self._diameter = 0


    def _create_ref_planet(self):
        self._ref_planet_plot = Ellipse((0, 0), width=self._diameter, height=self._diameter, fill=False, color='grey')
        self._axes.add_patch(self._ref_planet_plot)


    def update_ref_planet(self, telemetry):
        if self._ref_planet_name == telemetry.ref_body_name:
            return
        self._ref_planet_name = telemetry.ref_body_name
        self._diameter = PLANET_DATA[self._ref_planet_name]['radius'] *1000 * 2
        if not self._ref_planet_plot:
            self._create_ref_planet()
        else:
            self._ref_planet_plot.width = diameter
            self._ref_planet_plot.height = diameter


    def remove(self):
        if self._ref_planet_plot:
            self._ref_planet_plot.remove()
        self._ref_planet_plot = None
        self._ref_planet_name = None
        self._diameter = 0
