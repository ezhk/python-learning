#!/usr/bin/env python

from logging import getLogger
import sys
from threading import Thread

from PyQt5 import QtWidgets, QtCore

# PyInstaller depends
import sqlalchemy.ext.baked

from ui.mainWindow import MainWindow

import jim.logger
from jim.config import SERVER_ADDRESS, SERVER_PORT
from jim.classes import ServerThread, UsersExtension

from jim.utils import load_server_settings


def update_main_buttons(server, main_window):
    if server and server.alive():
        main_window.runButton.setDisabled(True)
        main_window.stopButton.setDisabled(False)
    else:
        main_window.runButton.setDisabled(False)
        main_window.stopButton.setDisabled(True)


if __name__ == "__main__":
    logger = getLogger("messenger.server")
    server = ServerThread(logger=logger)

    user_extenstion = UsersExtension()

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(user_extenstion)
    main_window.runButton.clicked.connect(server.start)
    main_window.stopButton.clicked.connect(server.stop)

    # update buttons behaviour
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: update_main_buttons(server, main_window))
    timer.timeout.connect(lambda: main_window.refresh_mainwindow())
    timer.start(500)

    sys.exit(app.exec())
