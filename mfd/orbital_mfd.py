from .ksp_mfd import KspMFD
from math import sqrt
import numpy as np
from matplotlib.patches import Ellipse, Circle

from planet_data import PLANET_DATA
from orbital_data import EllipseData, HyperboleData
from mfd.orbital_point import PeriapsisPlot, ApoapsisPlot, AscendingPlot, DescendingPlot, AscendingDescendingLine, VesselPlot



class OrbitalMFD(KspMFD):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        KspMFD.__init__(self, parent, width, height, dpi)
        self.show_legend = True
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


    def _update_mfd_data(self, telemetry):
        if self.ref_body_name != telemetry.ref_body_name.lower():
            self.ref_body_name = telemetry.ref_body_name.lower()
            self.draw_ref_planet(telemetry)
        self.draw_vessel_orbit(telemetry)
        self.numeric_orbit_value(telemetry)
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
        if self.hyperbole_orbit_plot:
            self.hyperbole_orbit_plot.pop(0).remove()
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
        if self.ellipse_orbit_plot:
            self.ellipse_orbit_plot.remove()
            self.ellipse_orbit_plot = None
        if self.hyperbole_orbit_plot:
            self.hyperbole_orbit_plot.pop(0).remove()
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
