from .ksp_mfd import KspMFD
from math import sqrt
import numpy as np
from matplotlib.patches import Ellipse, Circle
from matplotlib.lines import Line2D


PLANET_DATA = {
    # all values in km and corresponding
    'kerbol': {
        'name': "Kerbol",
        'mu': 1167922000,
        'radius': 65400,
        'color': "yellow"
    },
    'moho': {
        'name': "Moho",
        'parent': "Kerbol",
        'alt': 5263138.3,
        'mu': 245.25,
        'radius': 250,
        'inclination': 7,
        'soi': 11206.449,
        'color': "brown"
    },
    'eve': {
        'name': "Eve",
        'parent': "Kerbol",
        'alt': 9832684.544,
        'mu': 8171.73,
        'radius': 700,
        'inclination': 2.1,
        'soi': 85109.364,
        'color': "purple"
    },
    'gilly': {
        'name': "Gilly",
        'parent': "Eve",
        'alt': 31500,
        'mu': 0.008289450,
        'radius': 13,
        'inclination': 12,
        'soi': 126.123,
        'color': "brown"
        },
    'kerbin': {
        'name': "Kerbin",
        'parent': "kerbol",
        'alt': 13599840.256,
        'mu': 3531.6,
        'radius': 600,
        'inclination': 0,
        'soi': 84159.2865,
        'color': "skyblue"
    },
    'mun': {
        'name': "Mun",
        'parent': "Kerbin",
        'alt': 12000,
        'mu': 65.138,
        'radius': 200,
        'inclination': 0,
        'soi': 2430,
        'color': "gray"
    },
    'minmus': {
        'name': "Minmus",
        'parent': "Kerbin",
        'alt': 47000,
        'mu': 1.7658,
        'radius': 60,
        'inclination': 6,
        'soi': 2247.428,
        'color': "#97d0a9"
    },
    'duna': {
        'name': "Duna",
        'parent': "Kerbol",
        'alt': 20726155.264,
        'mu': 301.363,
        'radius': 320,
        'inclination': 1.85,
        'soi': 47921.949,
        'color': "orange"
    },
    'ike': {
        'name': "Ike",
        'parent': "Duna",
        'alt': 3200,
        'mu': 18.56837,
        'radius': 130,
        'inclination': 0.2,
        'soi': 1049.599,
        'color': "silver"
    },
    'Dres': {
        'name': "Dres",
        'parent': "Kerbol",
        'alt': 40839348.203,
        'mu': 21.4845,
        'radius': 138,
        'inclination': 5,
        'soi': 32832.84,
        'color': "silver"
    },
    'Jool': {
        'name': "Jool",
        'parent': "Kerbol",
        'alt': 68773560.320,
        'mu': 282528.0042,
        'radius': 6000,
        'inclination': 1.3,
        'soi': 2455985.185,
        'color': "green"
    },
    'Laythe': {
        'name': "Laythe",
        'parent': "Jool",
        'alt': 27184,
        'mu': 1962,
        'radius': 500,
        'inclination': 0,
        'soi': 3723.646,
        'color': "darkblue"
    },
    'Vall': {
        'name': "Vall",
        'parent': "Jool",
        'alt': 43152,
        'mu': 207.4815,
        'radius': 300,
        'inclination': 0,
        'soi': 2406.401,
        'color': "skyblue"
    },
    'Tylo': {
        'name': "Tylo",
        'parent': "Jool",
        'alt': 68500,
        'mu': 2825.28,
        'radius': 600,
        'inclination': 0.025,
        'soi': 10856.51837,
        'color': "beige"
    },
    'Bop': {
        'name': "Bop",
        'parent': "Jool",
        'alt': 104500,
        'mu': 2.486835,
        'radius': 65,
        'inclination': 15,
        'soi': 993.0028,
        'color': "brown"
    },
    'Pol': {
        'name': "Pol",
        'parent': "Jool",
        'alt': 129890,
        'mu': 0.227,
        'radius': 44,
        'inclination': 1.304,
        'soi': 2455985.185,
        'color': "orange"
    },
    'Eeloo': {
        'name': "Eeloo",
        'parent': "Kerbol",
        'alt': 90118858.179,
        'mu': 74.410815,
        'radius': 210,
        'inclination': 6.15,
        'soi': 119082.94,
        'color': "grey"
    } 
};

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
        if self.ref_body_name != telemetry['ref_body_name'].lower():
            self.ref_body_name = telemetry['ref_body_name'].lower()
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
        text.append('Pe  %s' % self.get_value_to_string_KM(telemetry['periapsis_altitude']))
        text.append('Ap  %s' % self.get_value_to_string_KM(telemetry['apoapsis_altitude']))
        text.append('Ecc %.4f' % telemetry['eccentricity'])
        text.append('T   %s' % self.get_value_to_string_KM(telemetry['period']))
        text.append('PeT %s' % self.get_value_to_string_KM(telemetry['time_to_periapsis']))
        text.append('ApT %s' % self.get_value_to_string_KM(telemetry['time_to_apoapsis']))
        text.append('Vel %s' % self.get_value_to_string_KM(telemetry['orbital_speed']))
        text.append('Inc %.4f°' % telemetry['inclination_deg'])
        text.append('LAN %.4f°' % telemetry['longitude_of_ascending_node_deg'])
        text.append('LPe %.4f°' % telemetry['argument_of_periapsis_deg'])
        leg_source = [self.ref_planet]*len(text)

        leg = self.axes.legend(leg_source, text, handlelength=0, handletextpad=0, fancybox=True, 
                                                 framealpha=0, loc='upper left',
                                                prop={'family':'monospace'})
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


    def compute_trajectory_parameter(self, telemetry):
        tlm = telemetry
        cos_longitude_of_ascending_node = np.cos(tlm['longitude_of_ascending_node'])
        sin_longitude_of_ascending_node = np.sin(tlm['longitude_of_ascending_node'])
        cos_longitude_of_periapsis = np.cos(tlm['argument_of_periapsis'] + tlm['longitude_of_ascending_node'])
        sin_longitude_of_periapsis = np.sin(tlm['argument_of_periapsis'] + tlm['longitude_of_ascending_node'])
        cos_argument_of_periapsis = np.cos(tlm['argument_of_periapsis'])

        self.trajectory_param = {}

        # Ellipse parameter
        c = (tlm['apoapsis'] - tlm['periapsis']) / 2.0
        self.trajectory_param['ellipse'] = None
        self.trajectory_param['parabole'] = None
        self.trajectory_param['hyperbole'] = None
        if tlm['eccentricity'] < 1:
            self.trajectory_param['ellipse'] = {}
            self.trajectory_param['ellipse']['focus_x'] = c * cos_longitude_of_periapsis
            self.trajectory_param['ellipse']['focus_y'] = c * sin_longitude_of_periapsis
            self.trajectory_param['ellipse']['width'] = 2 * tlm['semi_major_axis']
            self.trajectory_param['ellipse']['height'] = 2 * tlm['semi_minor_axis']
        elif tlm['eccentricity'] > 1:
            # for c3 : https://en.wikipedia.org/wiki/Hyperbolic_trajectory
            # for a, l, r : https://en.wikipedia.org/wiki/Characteristic_energy
            c3 = tlm['speed']**2 - 2 * PLANET_DATA[self.ref_body_name]['mu'] * 10**9 / tlm['radius']
            a = -PLANET_DATA[self.ref_body_name]['mu'] * 10**9 / c3
            l = a * (1 - tlm['eccentricity']**2)

            self.trajectory_param['hyperbole'] = {}
            limit_soi = np.arccos((l / (PLANET_DATA[self.ref_body_name]['soi']*1000*3) - 1) / tlm['eccentricity'])
            limit_asymp = np.arccos(-1/tlm['eccentricity'])
            limit = limit_soi if limit_soi < limit_asymp else limit_asymp
            t = np.linspace(-limit, limit, num=100)
            r = l / (1 + tlm['eccentricity'] * np.cos(t))
            xx = r * np.cos(t) 
            yy = r * np.sin(t)  
            self.trajectory_param['hyperbole']['x'] = xx * cos_longitude_of_periapsis - yy * sin_longitude_of_periapsis
            self.trajectory_param['hyperbole']['y'] = xx * sin_longitude_of_periapsis + yy * cos_longitude_of_periapsis

        self.trajectory_param['periapsis'] = {}
        self.trajectory_param['periapsis']['x'] = tlm['periapsis'] * cos_longitude_of_periapsis
        self.trajectory_param['periapsis']['y'] = tlm['periapsis'] * sin_longitude_of_periapsis

        self.trajectory_param['apoapsis'] = {}
        if tlm['eccentricity'] < 1: 
            self.trajectory_param['apoapsis']['x'] = -tlm['apoapsis'] * cos_longitude_of_periapsis
            self.trajectory_param['apoapsis']['y'] = -tlm['apoapsis'] * sin_longitude_of_periapsis
        else:
            self.trajectory_param['apoapsis'] = None

        p = tlm['semi_minor_axis']**2 / tlm['semi_major_axis'] if tlm['eccentricity'] < 1 else l
        ascending_node_radius = p / (1 + tlm['eccentricity'] * cos_argument_of_periapsis)
        descending_node_radius = p / (1 - tlm['eccentricity'] * cos_argument_of_periapsis)
        self.trajectory_param['ascending_node'] = {}
        self.trajectory_param['ascending_node']['x'] = ascending_node_radius * cos_longitude_of_ascending_node
        self.trajectory_param['ascending_node']['y'] = ascending_node_radius * sin_longitude_of_ascending_node

        self.trajectory_param['descending_node'] = {}
        self.trajectory_param['descending_node']['x'] = -descending_node_radius * cos_longitude_of_ascending_node # cos(x+pi)=-cos(x)
        self.trajectory_param['descending_node']['y'] = -descending_node_radius * sin_longitude_of_ascending_node # sin(x+pi)=-sin(x)

        self.trajectory_param['vessel'] = {}
        self.trajectory_param['vessel']['x'] = tlm['radius'] * np.cos(tlm['true_anomaly'] + tlm['argument_of_periapsis'] + tlm['longitude_of_ascending_node'])
        self.trajectory_param['vessel']['y'] = tlm['radius'] * np.sin(tlm['true_anomaly'] + tlm['argument_of_periapsis'] + tlm['longitude_of_ascending_node'])


    def draw_vessel_orbit(self, telemetry):
        self.compute_trajectory_parameter(telemetry)
        if telemetry['eccentricity'] < 1:
            self.draw_ellipse_orbit(telemetry)
        elif telemetry['eccentricity'] == 1:
            self.draw_parabole_orbit(telemetry)
        else:
            self.draw_hyperbole_orbit(telemetry)


    def draw_ellipse_orbit(self, telemetry):
        if self.hyperbole_orbit_plot:
            self.hyperbole_orbit_plot.pop(0).remove()
        trajectory_param = self.trajectory_param
        angle = telemetry['argument_of_periapsis_deg'] + telemetry['longitude_of_ascending_node_deg']
        if not self.ellipse_orbit_plot:
            self.ellipse_orbit_plot = Ellipse((-trajectory_param['ellipse']['focus_x'], -trajectory_param['ellipse']['focus_y']),
                                             width=trajectory_param['ellipse']['width'], height=trajectory_param['ellipse']['height'],
                                             angle=angle, fill=False, color='green')
            self.axes.add_patch(self.ellipse_orbit_plot)
        else:
            self.ellipse_orbit_plot.center = (-trajectory_param['ellipse']['focus_x'], -trajectory_param['ellipse']['focus_y'])
            self.ellipse_orbit_plot.width = trajectory_param['ellipse']['width']
            self.ellipse_orbit_plot.height = trajectory_param['ellipse']['height']
            self.ellipse_orbit_plot.angle = angle
        self.draw_periapsis(telemetry)
        self.draw_apoapsis(telemetry)
        self.draw_ascending_descending_node(telemetry)
        self.draw_vessel(telemetry)


    def draw_parabole_orbit(self, telemetry):
        pass


    def draw_hyperbole_orbit(self, telemetry):
        trajectory_param = self.trajectory_param
        if self.ellipse_orbit_plot:
            self.ellipse_orbit_plot.remove()
            self.ellipse_orbit_plot = None
        if self.hyperbole_orbit_plot:
            self.hyperbole_orbit_plot.pop(0).remove()
        self.hyperbole_orbit_plot = self.axes.plot(trajectory_param['hyperbole']['x'], trajectory_param['hyperbole']['y'],
                                                   color='green', linewidth=0.8)
        self.draw_periapsis(telemetry)
        self.draw_ascending_descending_node(telemetry)
        self.draw_vessel(telemetry)


    def draw_periapsis(self, telemetry):
        trajectory_param = self.trajectory_param
        if not self.periapsis_plot:
            # Plot periapsis position like a empty circle
            self.periapsis_plot = Line2D([trajectory_param['periapsis']['x']], [trajectory_param['periapsis']['y']],
                                            marker='o', markerfacecolor='black', markersize='6', color='green')
            self.axes.add_line(self.periapsis_plot)
        else:
            self.periapsis_plot.set_xdata([trajectory_param['periapsis']['x']])
            self.periapsis_plot.set_ydata([trajectory_param['periapsis']['y']])


    def draw_apoapsis(self, telemetry):
        trajectory_param = self.trajectory_param
        if not self.apoapsis_plot:
            # Plot apoapsis position like a filled circle
            self.apoapsis_plot = Line2D([trajectory_param['apoapsis']['x']], [trajectory_param['apoapsis']['y']], 
                                        marker='o', markersize='6', color='green')
            self.axes.add_line(self.apoapsis_plot)
        else:
            self.apoapsis_plot.set_xdata([trajectory_param['apoapsis']['x']])
            self.apoapsis_plot.set_ydata([trajectory_param['apoapsis']['y']])


    def draw_ascending_descending_node(self, telemetry):
        trajectory_param = self.trajectory_param
        if not self.ascending_plot:
            # Plot ascending node position like a filled square
            self.ascending_plot = Line2D([trajectory_param['ascending_node']['x']], [trajectory_param['ascending_node']['y']],
                                          marker='s', markersize='6', color='green')
            self.axes.add_line(self.ascending_plot)

            # Plot descending node position like a empy square
            self.descending_plot = Line2D([trajectory_param['descending_node']['x']], [trajectory_param['descending_node']['y']],
                                          marker='s', markerfacecolor='black', markersize='6', color='green')
            self.axes.add_line(self.descending_plot)

            # Plot dashed line between ascending and descending node
            self.ascending_descending = Line2D([trajectory_param['ascending_node']['x'], trajectory_param['descending_node']['x']],
                                               [trajectory_param['ascending_node']['y'], trajectory_param['descending_node']['y']], 
                                               linestyle='--', marker='None', color='green')
            self.axes.add_line(self.ascending_descending)
        else:
            self.ascending_plot.set_xdata([trajectory_param['ascending_node']['x']])
            self.ascending_plot.set_ydata([trajectory_param['ascending_node']['y']])

            self.descending_plot.set_xdata([trajectory_param['descending_node']['x']])
            self.descending_plot.set_ydata([trajectory_param['descending_node']['y']])

            self.ascending_descending.set_xdata([trajectory_param['ascending_node']['x'], trajectory_param['descending_node']['x']])
            self.ascending_descending.set_ydata([trajectory_param['ascending_node']['y'], trajectory_param['descending_node']['y']])


    def draw_vessel(self, telemetry):
        trajectory_param = self.trajectory_param
        if not self.vessel_plot:
            # Plot vessel position like a line between the center of mass of the ref body and the vessel position
            self.vessel_plot = Line2D([0, trajectory_param['vessel']['x']], [0, trajectory_param['vessel']['y']],
                                      marker='None', color='green')
            self.axes.add_line(self.vessel_plot)
        else:
            self.vessel_plot.set_xdata([0, trajectory_param['vessel']['x']])
            self.vessel_plot.set_ydata([0, trajectory_param['vessel']['y']])