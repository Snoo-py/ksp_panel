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


class ProjectionText(OrbitPointText):
    def update_text(self, projection_mode):
        _text = 'Prj: %s' % projection_mode.label
        OrbitPointText.update_text(self, _text)