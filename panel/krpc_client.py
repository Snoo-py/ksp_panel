from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot, QObject
import numpy as np
import krpc

from panel.telemetry.telemetry import Telemetry



class KrpcClient(QObject):
    ksp_connected = pyqtSignal()
    ksp_disconnected = pyqtSignal()
    telemetry_updated = pyqtSignal(Telemetry)

    def __init__(self, server_address, **kwargs):
        super(KrpcClient, self).__init__(**kwargs)

        self.server_address = server_address

        self.ksp_is_connected = False
        self.ksp_current_game_scene = None
        self.as_active_vessel = False

        # initialize update timers
        self._short_term_scheduler = QTimer()
        self._short_term_scheduler.timeout.connect(self.short_term_processing)
        self._short_term_scheduler.start(int(0.25 * 100))


    @pyqtSlot()
    def connect_to_ksp(self):
        try:
            self.ksp_conn = krpc.connect(address=self.server_address)
            self.ksp_is_connected = True
            self.ksp_connected.emit()
            print('Connection Success')
        except OSError:
            print('Connection error')
            self.ksp_is_connected = False
            return


    @pyqtSlot()
    def short_term_processing(self):
        if self.ksp_is_connected:
            # Check if the current game scene is a a Flight scene, continue processing
            if self.ksp_conn.krpc.current_game_scene == self.ksp_conn.krpc.GameScene.flight:
                # set up telemetry for the vessel if it hasn't already been done
                if not self.as_active_vessel:
                    self.init_telemetry()
                else:
                    self.update_telemetry()
            else:
                # otherwise, unset the active vessel and telemetry
                self.as_active_vessel = False


    def init_telemetry(self):
        self.space_center = self.ksp_conn.space_center
        self.as_active_vessel = True
        self.telemetry = Telemetry()


    def update_telemetry(self):
        self.telemetry.update_from_krpc_active_vessel(self.space_center.ut, self.space_center.active_vessel)
        self.telemetry_updated.emit(self.telemetry)
