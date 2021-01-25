from math import sqrt
import numpy as np
from matplotlib.patches import Ellipse, Circle

from panel.mfd.ksp_mfd_figure import KspMFDFigure
from panel.planet_data import PLANET_DATA
from panel.orbital.hyperbole_orbit import HyperboleOrbit
from panel.orbital.ellipse_orbit import EllipseOrbit
from panel.orbital.orbital_point import PeriapsisPlot, ApoapsisPlot, AscendingPlot, DescendingPlot, AscendingDescendingLine, VesselPlot



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
        self.show_legend = True
        self.show_orbit = True
        self.current_active_vessel_id = None
        self.ref_planet = None
        self.ref_body_name = None
        self.ellipse_orbit_plot = EllipseOrbit(self.axes)
        self.hyperbole_orbit_plot = HyperboleOrbit(self.axes)
        self.periapsis_plot = PeriapsisPlot(self.axes)
        self.apoapsis_plot = ApoapsisPlot(self.axes)
        self.ascending_plot = AscendingPlot(self.axes)
        self.descending_plot = DescendingPlot(self.axes)
        self.ascending_descending = AscendingDescendingLine(self.axes)
        self.vessel_plot = VesselPlot(self.axes)
        self.ship_text = None


    def _update_mfd_data(self, telemetry):
        if self.show_orbit:
            self.draw_ref_planet(telemetry)
            self.draw_vessel_orbit(telemetry)
        else:
            self.remove_orbit_display()
        if self.show_legend:
            self.numeric_orbit_value(telemetry)
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


    def draw_ref_planet(self, telemetry):
        # Reference planet
        if self.ref_body_name == telemetry.ref_body_name:
            return
        self.ref_body_name = telemetry.ref_body_name
        diameter = PLANET_DATA[self.ref_body_name]['radius'] *1000 * 2
        if not self.ref_planet:
            self.ref_planet = Ellipse((0, 0), width=diameter, height=diameter, fill=False, color='grey')
            self.axes.add_patch(self.ref_planet)
        else:
            self.ref_planet.width = diameter
            self.ref_planet.height = diameter
        limit = PLANET_DATA[self.ref_body_name]['soi']*1000


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
        self.periapsis_plot.update_plot(ellipse)
        self.apoapsis_plot.update_plot(ellipse)
        self.ascending_plot.update_plot(ellipse)
        self.descending_plot.update_plot(ellipse)
        self.ascending_descending.update_plot(ellipse)
        self.vessel_plot.update_plot(ellipse)


    def draw_parabole_orbit(self, telemetry):
        pass


    def draw_hyperbole_orbit(self, telemetry):
        self.ellipse_orbit_plot.remove()
        self.hyperbole_orbit_plot.update_orbit(telemetry)
        self.periapsis_plot.update_plot(telemetry)
        self.ascending_plot.update_plot(telemetry)
        self.descending_plot.update_plot(telemetry)
        self.ascending_descending.update_plot(telemetry)
        self.vessel_plot.update_plot(telemetry)


    def remove_text(self):
        if self.ship_text:
            self.ship_text.remove()
            self.ship_text = None


    def remove_orbit_display(self):
        self.remove_reference_planet()
        self.ellipse_orbit_plot.remove()
        self.hyperbole_orbit_plot.remove()
        self.remove_parabole_orbit()
        self.periapsis_plot.remove()
        self.apoapsis_plot.remove()
        self.ascending_plot.remove()
        self.descending_plot.remove()
        self.ascending_descending.remove()
        self.vessel_plot.remove()


    def remove_reference_planet(self):
        if self.ref_planet:
            self.ref_planet.remove()
            self.ref_planet = None
            self.ref_body_name = None


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
        pass
