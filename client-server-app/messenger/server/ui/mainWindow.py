# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from .historyDialog import HistoryDialog
from .settingsDialog import SettingsDialog


class MainWindow(object):
    def __init__(self, users_extension):
        super().__init__()

        self.users_extension = users_extension
        self.window_object = QtWidgets.QMainWindow()

        # define buttons vehaviour
        self.button_actions = {}
        self.define_button_actions(self.window_object)

        # init table state
        self.activeUsersView = QtWidgets.QTableView()

        # create window and show it
        self.setupUi(self.window_object)
        self.window_object.show()

    def get_active_users_model(self):
        table = QtGui.QStandardItemModel()
        table.setHorizontalHeaderLabels(
            ["Username", "IP address", "Port", "Last access"]
        )
        for user in self.users_extension.active_users:
            row = []
            for key in ("username", "address", "port", "atime"):
                value = QtGui.QStandardItem(str(user.get(key)))
                value.setEditable(False)
                row.append(value)
            table.appendRow(row)
        return table

    def define_button_actions(self, MainWindow):
        def _exit_action():
            QtWidgets.qApp.quit()

        def _refresh_action():
            self.activeUsersView.setModel(self.get_active_users_model())

        def _history_action():
            HistoryDialog(self.users_extension)

        def _settings_action():
            SettingsDialog()

        # exit action
        self.button_actions.update(
            {"exit": QtWidgets.QAction("Exit", MainWindow)}
        )
        self.button_actions["exit"].setShortcut("Ctrl+Q")
        self.button_actions["exit"].triggered.connect(_exit_action)

        # refresh action
        self.button_actions.update(
            {"refresh": QtWidgets.QAction("Refresh", MainWindow)}
        )
        self.button_actions["refresh"].triggered.connect(_refresh_action)

        # refresh action
        self.button_actions.update(
            {"history": QtWidgets.QAction("History", MainWindow)}
        )
        self.button_actions["history"].triggered.connect(_history_action)

        # refresh action
        self.button_actions.update(
            {"settings": QtWidgets.QAction("Settings", MainWindow)}
        )
        self.button_actions["settings"].triggered.connect(_settings_action)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 640)
        self.usersWidget = QtWidgets.QWidget(MainWindow)
        self.usersWidget.setObjectName("usersWidget")
        MainWindow.setCentralWidget(self.usersWidget)

        self.toolbar = MainWindow.addToolBar("ToolBar")
        for _, action in self.button_actions.items():
            self.toolbar.addAction(action)

        self.label = QtWidgets.QLabel(self.usersWidget)
        self.label.setGeometry(QtCore.QRect(200, 10, 81, 21))
        self.label.setObjectName("tableName")

        self.activeUsersView = QtWidgets.QTableView(self.usersWidget)
        self.activeUsersView.setGeometry(QtCore.QRect(10, 40, 461, 501))
        self.activeUsersView.setObjectName("activeUsersView")
        self.activeUsersView.horizontalHeader().setStretchLastSection(True)

        # fill table by users data
        self.activeUsersView.setModel(self.get_active_users_model())
        self.activeUsersView.resizeColumnsToContents()
        self.activeUsersView.resizeRowsToContents()

        self.runButton = QtWidgets.QPushButton(self.usersWidget)
        self.runButton.setGeometry(QtCore.QRect(40, 560, 171, 41))
        self.runButton.setObjectName("runButton")

        self.stopButton = QtWidgets.QPushButton(self.usersWidget)
        self.stopButton.setGeometry(QtCore.QRect(270, 560, 171, 41))
        self.stopButton.setObjectName("stopButton")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Server"))
        self.runButton.setText(_translate("MainWindow", "Run server"))
        self.stopButton.setText(_translate("MainWindow", "Stop server"))
        self.label.setText(_translate("MainWindow", "Active users"))
