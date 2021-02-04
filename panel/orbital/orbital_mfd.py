from panel.mfd.ksp_mfd_figure import KspMFDFigure
from panel.orbital.ref_planet_plot import RefPlanetPlot
from panel.orbital.hyperbole_orbit import HyperboleOrbit
from panel.orbital.ellipse_orbit import EllipseOrbit
from panel.telemetry.telemetry import PROJECTION
from panel.orbital.orbital_text import ProjectionText, ShipOrbitalText



class OrbitalMFD(KspMFDFigure):
    _buttons = {
        'L1': {
            'text': 'DST',
            'handler': 'handler_toggle_distance_unit'
        },
        'L2': {
            'text': 'MOD',
            'handler': 'handler_toggle_display_mode'
        },
        'L3': {
            'text': 'PRJ',
            'handler': 'handler_toggle_projection_mode'
        },
    }

    DISPLAY_MODE = ['all', 'legend', 'orbit']

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        KspMFDFigure.__init__(self, parent, width, height, dpi)
        self.display_mode_idx = 0
        self.projection_mode = PROJECTION.SHIP
        self.show_legend = True
        self.show_orbit = True
        self.current_active_vessel_id = None
        self.ref_planet_plot = RefPlanetPlot(self.axes)
        self.ellipse_orbit_plot = EllipseOrbit(self.axes)
        self.hyperbole_orbit_plot = HyperboleOrbit(self.axes)
        self.ship_text = ShipOrbitalText(self.axes, 0.05, 0.95, color='green', verticalalignment='top',
                                         transform=self.axes.transAxes, fontsize=14)
        self.projection_text = ProjectionText(self.axes, 0.85, 0.95, color='grey',
                                              transform=self.axes.transAxes, fontsize=14)


    def _update_mfd_data(self, telemetry):
        telemetry.projection_mode = self.projection_mode
        if self.show_orbit:
            self.ref_planet_plot.update_ref_planet(telemetry)
            self.draw_vessel_orbit(telemetry)
        else:
            self.remove_orbit_display()
        if self.show_legend:
            self.ship_text.update_text(telemetry)
            self.projection_text.update_text(self.projection_mode)
        else:
            self.remove_text()
        self.axes.axis('auto')
        self.axes.set_aspect('equal', adjustable='datalim')
        self.axes.relim()


    def draw_vessel_orbit(self, telemetry):
        if telemetry.eccentricity < 1:
            self.draw_ellipse_orbit(telemetry)
        elif telemetry.eccentricity == 1:
            self.draw_parabole_orbit(telemetry)
        else:
            self.draw_hyperbole_orbit(telemetry)


    def draw_ellipse_orbit(self, ellipse):
        self.hyperbole_orbit_plot.remove()
        self.ellipse_orbit_plot.update_orbit(ellipse)


    def draw_parabole_orbit(self, telemetry):
        pass


    def draw_hyperbole_orbit(self, telemetry):
        self.ellipse_orbit_plot.remove()
        self.hyperbole_orbit_plot.update_orbit(telemetry)


    def remove_text(self):
        self.ship_text.remove()
        self.projection_text.remove()


    def remove_orbit_display(self):
        self.ref_planet_plot.remove()
        self.ellipse_orbit_plot.remove()
        self.hyperbole_orbit_plot.remove()
        self.remove_parabole_orbit()


    def remove_parabole_orbit(self):
        pass


    def handler_toggle_distance_unit(self):
        pass


    def handler_toggle_display_mode(self):
        self.display_mode_idx = (self.display_mode_idx + 1) % len(self.DISPLAY_MODE)
        mode = self.DISPLAY_MODE[self.display_mode_idx]
        if mode == 'all':
            self.show_legend = True
            self.show_orbit = True
        elif mode == 'orbit':
            self.show_legend = False
            self.show_orbit = True
        elif mode == 'legend':
            self.show_legend = True
            self.show_orbit = False


    def handler_toggle_projection_mode(self):
        self.projection_mode = self.projection_mode.next()
