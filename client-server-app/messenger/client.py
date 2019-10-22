#!/usr/bin/env python

from logging import getLogger

from PyQt5 import QtWidgets, QtCore
import sys

sys.path.append(".")


from ui.client.autorizeDialog import AuthorizeDialog
from ui.client.mainWindow import MainWindow

from jim.classes import Client
from jim.utils import parse_arguments
import jim.logger


if __name__ == "__main__":
    opts = parse_arguments()
    username = opts.username

    app = QtWidgets.QApplication(sys.argv)
    if not username:
        authorize_gialog = AuthorizeDialog()
        app.exec_()

        username = authorize_gialog.get_username() or sys.exit()

    client = Client(opts.address, opts.port, username, logger=getLogger("messenger.client"))
    main_window = MainWindow(client)
    main_window.bind_signals()

    client.start()
    app.exec_()

    try:
        client.stop()
        client.join()
    except Exception:
        pass
