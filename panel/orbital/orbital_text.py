from panel.telemetry.telemetry import PROJECTION

class OrbitPointText(object):
    def __init__(self, axes, x, y, *args, **kwargs):
        self._axes = axes
        self._args = args
        self._kwargs = kwargs
        self._x = x
        self._y = y
        self._text = None


    def _create_text(self, text):
        self._text = self._axes.text(self._x, self._y, text, *self._args, **self._kwargs)


    def update_text(self, text):
        if not self._text:
            self._create_text(text)
        else:
            self._text.set_text(text)


    def remove(self):
        if self._text:
            self._text.remove()
            self._text = None



class ShipOrbitalText(OrbitPointText):
    def update_text(self, telemetry):
        _text = []
        _text.append('----SELF----')
        _text.append('Pe  %s' % telemetry.periapsis_altitude_str)
        _text.append('Ap  %s' % telemetry.apoapsis_altitude_str)
        _text.append('Rad %s' % telemetry.radius_altitude_str)
        _text.append('Ecc %.4f' % telemetry.eccentricity)
        _text.append('T   %s' % telemetry.period_str)
        _text.append('PeT %s' % telemetry.time_to_periapsis_str)
        _text.append('ApT %s' % telemetry.time_to_apoapsis_str)
        _text.append('Vel %s' % telemetry.orbital_speed_str)
        _text.append('Inc %.4f°' % telemetry.inclination_deg)
        _text.append('LAN %.4f°' % telemetry.longitude_of_ascending_node_deg)
        _text.append('LPe %.4f°' % telemetry.longitude_of_periapsis_deg)
        _text.append('AgP %.4f°' % telemetry.argument_of_periapsis_deg)
        _text.append('Tra %.4f°' % telemetry.true_anomaly)
        _text.append('Mna %.4f°' % telemetry.mean_anomaly)
        _text = '\n'.join(_text)
        OrbitPointText.update_text(self, _text)



class ProjectionText(OrbitPointText):
    def update_text(self, projection_mode):
        _text = 'Prj: %s' % projection_mode.label
        OrbitPointText.update_text(self, _text)