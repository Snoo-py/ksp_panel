#!/usr/bin/python3

import sys
import argparse
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread

import krpc

from panel.krpc_client import KrpcClient
from panel.telemetry.telemetry import Telemetry
from panel.orbital.orbital_mfd import OrbitalMFD
from panel.mfd.ksp_mfd_button import KspMFDButton



class Interface(QMainWindow):
    krpc_client_begin_connect = pyqtSignal()
    ksp_connected = pyqtSignal()
    ksp_disconnected = pyqtSignal()

    def __init__(self, ksp_ip):
        QMainWindow.__init__(self)
        self.setWindowTitle("Kerbal nav")

        self.orbital = OrbitalMFD(None, width=5, height=5)
        self.mfd = KspMFDButton(self, self.orbital, width=7, height=7)
        self.mfd.move(0, 0)

        self.showMaximized()

        self.ksp_thread = QThread()
        self.ksp_client = KrpcClient(ksp_ip)
        self.ksp_client.moveToThread(self.ksp_thread)

        self.krpc_client_begin_connect.connect(self.ksp_client.connect_to_ksp)
        self.ksp_client.telemetry_updated.connect(self.telemetry_updated)

        self.ksp_thread.start()

        self.krpc_client_begin_connect.emit()


    @pyqtSlot(Telemetry)
    def telemetry_updated(self, telemetry_data):
        self.orbital.update_mfd(telemetry_data)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', help='ksp server', required=True)
    args = parser.parse_args()

    app = QApplication(sys.argv)
    i = Interface(args.host)
    sys.exit(app.exec_())