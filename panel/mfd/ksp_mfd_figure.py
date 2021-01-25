from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class KspMFDFigure(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='black')

        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        self.axes.set_axis_off()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.ksp_disconnect = True


    def update_mfd(self, telemetry):
        """if not ksp_conn:
            self.error_text("ERR: NO CONNECTION")
        elif not ksp_conn.active_vessel:
            self.error_text('ERR: NO DATA')
        else:"""
        self._update_mfd_data(telemetry)
        self.draw()


    def _update_mfd_data(self, telemetry):
        pass


    def disconnect(self):
        self.ksp_disconnect = True


    def connect(self):
        self.ksp_disconnect = False


    def error_text(self, text):
        self.axes.text(0.5, 0.5, text,
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=self.axes.transAxes,
                       family='monospace',
                       color='red')


    def get_button_info(self, button_name):
        info = self._buttons.get(button_name)
        if not info:
            return '', None
        return info['text'], getattr(self, info['handler'])
