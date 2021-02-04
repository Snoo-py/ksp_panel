from panel.mfd.ksp_mfd_figure import KspMFDFigure
from panel.orbital.ref_planet_plot import RefPlanetPlot
from panel.orbital.hyperbole_orbit import HyperboleOrbit
from panel.orbital.ellipse_orbit import EllipseOrbit
from panel.telemetry.telemetry import PROJECTION
from panel.orbital.orbital_text import ProjectionText



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
        self.ship_text = None
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
            self.numeric_orbit_value(telemetry)
            self.projection_text.update_text(self.projection_mode)
        else:
            self.remove_text()
        self.axes.axis('auto')
        self.axes.set_aspect('equal', adjustable='datalim')
        self.axes.relim()


    def numeric_orbit_value(self, telemetry):
        text = []
        text.append('----SELF----')
        text.append('Pe  %s' % telemetry.periapsis_altitude_str)
        text.append('Ap  %s' % telemetry.apoapsis_altitude_str)
        text.append('Rad %s' % telemetry.radius_altitude_str)
        text.append('Ecc %.4f' % telemetry.eccentricity)
        text.append('T   %s' % telemetry.period_str)
        text.append('PeT %s' % telemetry.time_to_periapsis_str)
        text.append('ApT %s' % telemetry.time_to_apoapsis_str)
        text.append('Vel %s' % telemetry.orbital_speed_str)
        text.append('Inc %.4f°' % telemetry.inclination_deg)
        text.append('LAN %.4f°' % telemetry.longitude_of_ascending_node_deg)
        text.append('LPe %.4f°' % telemetry.longitude_of_periapsis_deg)
        text.append('AgP %.4f°' % telemetry.argument_of_periapsis_deg)
        text.append('Tra %.4f°' % telemetry.true_anomaly)
        text.append('Mna %.4f°' % telemetry.mean_anomaly)
        text = '\n'.join(text)
        if not self.ship_text:
            self.ship_text = self.axes.text(0.05, 0.95, text, horizontalalignment='left',
                                            verticalalignment='top', color='green',
                                            transform=self.axes.transAxes, fontsize=14)
        else:
            self.ship_text.set_text(text)


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
        if self.ship_text:
            self.ship_text.remove()
            self.ship_text = None


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
