# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


import sys

sys.path.append(".")

from PyQt5 import QtCore, QtWidgets
from jim.utils import load_server_settings, save_server_settings


class SettingsDialog(object):
    def __init__(self):
        super().__init__()
        self.config = load_server_settings()

        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.exec()

    def store_values(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Save settings")
        try:
            save_server_settings(
                self.addressEdit.text(),
                self.portEdit.text(),
                self.storageEdit.text(),
            )
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Settings has beed successfully saved")
        except Exception as err:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(f"Settings not saved: {err}")
        msg.exec()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 200)

        self.addressEdit = QtWidgets.QLineEdit(Dialog)
        self.addressEdit.setGeometry(QtCore.QRect(170, 20, 161, 21))
        self.addressEdit.setObjectName("addressEdit")
        self.addressEdit.insert(self.config["address"])

        self.portEdit = QtWidgets.QLineEdit(Dialog)
        self.portEdit.setGeometry(QtCore.QRect(170, 60, 161, 21))
        self.portEdit.setObjectName("portEdit")
        self.portEdit.insert(str(self.config["port"]))

        self.storageEdit = QtWidgets.QLineEdit(Dialog)
        self.storageEdit.setGeometry(QtCore.QRect(170, 100, 161, 21))
        self.storageEdit.setObjectName("dbNameEdit")
        self.storageEdit.insert(self.config["storage"])

        self.labelAddress = QtWidgets.QLabel(Dialog)
        self.labelAddress.setGeometry(QtCore.QRect(90, 20, 51, 21))
        self.labelAddress.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.labelAddress.setObjectName("labelAddress")
        self.labelPort = QtWidgets.QLabel(Dialog)
        self.labelPort.setGeometry(QtCore.QRect(110, 60, 31, 21))
        self.labelPort.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.labelPort.setObjectName("labelPort")
        self.labelStorage = QtWidgets.QLabel(Dialog)
        self.labelStorage.setGeometry(QtCore.QRect(40, 100, 101, 21))
        self.labelStorage.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.labelStorage.setObjectName("labelStorage")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 140, 161, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.store_values)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.labelAddress.setText(_translate("Dialog", "Address"))
        self.labelPort.setText(_translate("Dialog", "Port"))
        self.labelStorage.setText(_translate("Dialog", "Storage name"))
        self.pushButton.setText(_translate("Dialog", "Save"))
