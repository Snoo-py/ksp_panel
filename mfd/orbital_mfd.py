from .ksp_mfd import KspMFD
from math import sqrt
import numpy as np
from matplotlib.patches import Ellipse, Circle
from matplotlib.lines import Line2D

from planet_data import PLANET_DATA
from orbital_data import EllipseData, HyperboleData


class OrbitalMFD(KspMFD):

    def __init__(self, parent=None, width=5, height=5, dpi=100):
        KspMFD.__init__(self, parent, width, height, dpi)
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


    def get_value_to_string_KM(self, value):
        """
        10 -> 10
        100 -> 100
        1,000 -> 1.000K
        10,000 -> 10.00K
        100,000 -> 100.0K
        1,000,000 -> 1.000M
        10,000,000 -> 10.00M
        100,000,000 -> 100.0M
        """
        i_value = float(value)
        n = 1
        unit = None
        if i_value < 0:
            n = -1
            i_value = -i_value

        if i_value < 1000.0:
            v = '%s' % (n * i_value)
        elif i_value < 1000000.0:
            v = '%s' % (n * i_value / 1000.0)
            unit = 'K'
        else:
            v = '%s' % (n * i_value / 1000000.0)
            unit = 'M'
        if unit:
            return '%s%s' % (v[:5], unit)
        return '%s' % v[:6]


    def numeric_orbit_value(self, telemetry):
        text = []
        text.append('----SELF----')
        text.append('Pe  %s' % self.get_value_to_string_KM(telemetry.periapsis_altitude))
        text.append('Ap  %s' % self.get_value_to_string_KM(telemetry.apoapsis_altitude))
        text.append('Ecc %.4f' % telemetry.eccentricity)
        text.append('T   %s' % self.get_value_to_string_KM(telemetry.period))
        text.append('PeT %s' % self.get_value_to_string_KM(telemetry.time_to_periapsis))
        text.append('ApT %s' % self.get_value_to_string_KM(telemetry.time_to_apoapsis))
        text.append('Vel %s' % self.get_value_to_string_KM(telemetry.orbital_speed))
        text.append('Inc %.4f°' % telemetry.inclination_deg)
        text.append('LAN %.4f°' % telemetry.longitude_of_ascending_node_deg)
        text.append('LPe %.4f°' % telemetry.argument_of_periapsis_deg)
        leg_source = [self.ref_planet]*len(text)

        leg = self.axes.legend(leg_source, text, handlelength=0, handletextpad=0, fancybox=True,
                               framealpha=0, loc='upper left', prop={'family':'monospace'})
        for item in leg.legendHandles:
            item.set_visible(False)
        for item in leg.get_texts():
            item.set_color('green')


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
            # Plot periapsis position like a empty circle
            self.periapsis_plot = Line2D([telemetry.periapsis_x], [telemetry.periapsis_y],
                                            marker='o', markerfacecolor='black', markersize='6', color='green')
            self.axes.add_line(self.periapsis_plot)
        else:
            self.periapsis_plot.set_xdata([telemetry.periapsis_x])
            self.periapsis_plot.set_ydata([telemetry.periapsis_y])


    def draw_apoapsis(self, telemetry):
        if not self.apoapsis_plot:
            # Plot apoapsis position like a filled circle
            self.apoapsis_plot = Line2D([telemetry.apoapsis_x], [telemetry.apoapsis_y],
                                        marker='o', markersize='6', color='green')
            self.axes.add_line(self.apoapsis_plot)
        else:
            self.apoapsis_plot.set_xdata([telemetry.apoapsis_x])
            self.apoapsis_plot.set_ydata([telemetry.apoapsis_y])


    def draw_ascending_descending_node(self, telemetry):
        if not self.ascending_plot:
            # Plot ascending node position like a filled square
            self.ascending_plot = Line2D([telemetry.ascending_node_x], [telemetry.ascending_node_y],
                                          marker='s', markersize='6', color='green')
            self.axes.add_line(self.ascending_plot)

            # Plot descending node position like a empy square
            self.descending_plot = Line2D([telemetry.descending_node_x], [telemetry.descending_node_y],
                                          marker='s', markerfacecolor='black', markersize='6', color='green')
            self.axes.add_line(self.descending_plot)

            # Plot dashed line between ascending and descending node
            self.ascending_descending = Line2D([telemetry.ascending_node_x, telemetry.descending_node_x],
                                               [telemetry.ascending_node_y, telemetry.descending_node_y],
                                               linestyle='--', marker='None', color='green')
            self.axes.add_line(self.ascending_descending)
        else:
            self.ascending_plot.set_xdata([telemetry.ascending_node_x])
            self.ascending_plot.set_ydata([telemetry.ascending_node_y])

            self.descending_plot.set_xdata([telemetry.descending_node_x])
            self.descending_plot.set_ydata([telemetry.descending_node_y])

            self.ascending_descending.set_xdata([telemetry.ascending_node_x, telemetry.descending_node_x])
            self.ascending_descending.set_ydata([telemetry.ascending_node_y, telemetry.descending_node_y])


    def draw_vessel(self, telemetry):
        if not self.vessel_plot:
            # Plot vessel position like a line between the center of mass of the ref body and the vessel position
            self.vessel_plot = Line2D([0, telemetry.vessel_x], [0, telemetry.vessel_y],
                                      marker='None', color='green')
            self.axes.add_line(self.vessel_plot)
        else:
            self.vessel_plot.set_xdata([0, telemetry.vessel_x])
            self.vessel_plot.set_ydata([0, telemetry.vessel_y])