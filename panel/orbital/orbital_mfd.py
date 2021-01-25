from math import sqrt
import numpy as np
from matplotlib.patches import Ellipse, Circle

from panel.mfd.ksp_mfd_figure import KspMFDFigure
from panel.planet_data import PLANET_DATA
from panel.telemetry.ellipse import EllipseData
from panel.telemetry.hyperbole import HyperboleData
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
        self.ellipse_orbit_plot = None
        self.hyperbole_orbit_plot = None
        self.periapsis_plot = None
        self.apoapsis_plot = None
        self.ascending_plot = None
        self.descending_plot = None
        self.ascending_descending = None
        self.vessel_plot = None
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
            telemetry.__class__ = EllipseData
            self.draw_ellipse_orbit(telemetry)
        elif telemetry.eccentricity == 1:
            self.draw_parabole_orbit(telemetry)
        else:
            telemetry.__class__ = HyperboleData
            self.draw_hyperbole_orbit(telemetry)


    def draw_ellipse_orbit(self, ellipse):
        self.remove_hyperbole_orbit()
        angle = ellipse.argument_of_periapsis_deg + ellipse.longitude_of_ascending_node_deg
        if not self.ellipse_orbit_plot:
            self.ellipse_orbit_plot = Ellipse((-ellipse.focus_x, -ellipse.focus_y),
                                              width=ellipse.width, height=ellipse.height,
                                              angle=angle, fill=False, color='green')
            self.axes.add_patch(self.ellipse_orbit_plot)
        else:
            self.ellipse_orbit_plot.center = (-ellipse.focus_x, -ellipse.focus_y)
            self.ellipse_orbit_plot.width = ellipse.width
            self.ellipse_orbit_plot.height = ellipse.height
            self.ellipse_orbit_plot.angle = angle
        self.draw_periapsis(ellipse)
        self.draw_apoapsis(ellipse)
        self.draw_ascending_descending_node(ellipse)
        self.draw_vessel(ellipse)


    def draw_parabole_orbit(self, telemetry):
        pass


    def draw_hyperbole_orbit(self, telemetry):
        self.remove_ellipse_orbit()
        self.remove_hyperbole_orbit()
        self.hyperbole_orbit_plot = self.axes.plot(telemetry.hyperbole_x, telemetry.hyperbole_y,
                                                   color='green', linewidth=0.8)
        self.draw_periapsis(telemetry)
        self.draw_ascending_descending_node(telemetry)
        self.draw_vessel(telemetry)


    def draw_periapsis(self, telemetry):
        if not self.periapsis_plot:
            self.periapsis_plot = PeriapsisPlot(telemetry.periapsis_x, telemetry.periapsis_y)
            self.axes.add_line(self.periapsis_plot)
        else:
            self.periapsis_plot.update_plot(telemetry.periapsis_x, telemetry.periapsis_y)


    def draw_apoapsis(self, telemetry):
        if not self.apoapsis_plot:
            self.apoapsis_plot = ApoapsisPlot(telemetry.apoapsis_x, telemetry.apoapsis_y)
            self.axes.add_line(self.apoapsis_plot)
        else:
            self.apoapsis_plot.update_plot(telemetry.apoapsis_x, telemetry.apoapsis_y)


    def draw_ascending_descending_node(self, telemetry):
        if not self.ascending_plot:
            self.ascending_plot = AscendingPlot(telemetry.ascending_node_x ,telemetry.ascending_node_y)
            self.axes.add_line(self.ascending_plot)

            self.descending_plot = DescendingPlot(telemetry.descending_node_x, telemetry.descending_node_y)
            self.axes.add_line(self.descending_plot)

            self.ascending_descending = AscendingDescendingLine([telemetry.ascending_node_x, telemetry.descending_node_x],
                                                                [telemetry.ascending_node_y, telemetry.descending_node_y])
            self.axes.add_line(self.ascending_descending)
        else:
            self.ascending_plot.update_plot(telemetry.ascending_node_x, telemetry.ascending_node_y)
            self.descending_plot.update_plot(telemetry.descending_node_x, telemetry.descending_node_y)
            self.ascending_descending.update_plot([telemetry.ascending_node_x, telemetry.descending_node_x],
                                                  [telemetry.ascending_node_y, telemetry.descending_node_y])


    def draw_vessel(self, telemetry):
        if not self.vessel_plot:
            self.vessel_plot = VesselPlot(telemetry.vessel_x, telemetry.vessel_y)
            self.axes.add_line(self.vessel_plot)
        else:
            self.vessel_plot.update_plot(telemetry.vessel_x, telemetry.vessel_y)


    def remove_text(self):
        if self.ship_text:
            self.ship_text.remove()
            self.ship_text = None


    def remove_orbit_display(self):
        self.remove_reference_planet()
        self.remove_ellipse_orbit()
        self.remove_hyperbole_orbit()
        self.remove_parabole_orbit()
        self.remove_apoapsis()
        self.remove_periapsis()
        self.remove_ascending_descending()
        self.remove_vessel()


    def remove_reference_planet(self):
        if self.ref_planet:
            self.ref_planet.remove()
            self.ref_planet = None
            self.ref_body_name = None


    def remove_ellipse_orbit(self):
        if self.ellipse_orbit_plot:
            self.ellipse_orbit_plot.remove()
            self.ellipse_orbit_plot = None


    def remove_hyperbole_orbit(self):
        if self.hyperbole_orbit_plot:
            self.hyperbole_orbit_plot.pop(0).remove()
            self.hyperbole_orbit_plot = None


    def remove_parabole_orbit(self):
        pass


    def remove_periapsis(self):
        if self.periapsis_plot:
            self.periapsis_plot.remove()
            self.periapsis_plot = None


    def remove_apoapsis(self):
        if self.apoapsis_plot:
            self.apoapsis_plot.remove()
            self.apoapsis_plot = None


    def remove_ascending_descending(self):
        if self.ascending_plot:
            self.ascending_plot.remove()
            self.ascending_plot = None
        if self.descending_plot:
            self.descending_plot.remove()
            self.descending_plot = None
        if self.ascending_descending:
            self.ascending_descending.remove()
            self.ascending_descending = None


    def remove_vessel(self):
        if self.vessel_plot:
            self.vessel_plot.remove()
            self.vessel_plot = None


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
