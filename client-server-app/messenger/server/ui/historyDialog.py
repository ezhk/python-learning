# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historyDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class HistoryDialog(object):
    def __init__(self, users_extension):
        super().__init__()
        self.users_extension = users_extension

        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def get_history_model(self):
        table = QtGui.QStandardItemModel()
        table.setHorizontalHeaderLabels(
            ["Username", "IP address", "Port", "Connect time"]
        )
        for user in self.users_extension.users_history:
            row = []
            for key in ("username", "address", "port", "ctime"):
                value = QtGui.QStandardItem(str(user.get(key)))
                value.setEditable(False)
                row.append(value)
            table.appendRow(row)
        return table

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 640)
        self.historyView = QtWidgets.QTableView(Dialog)
        self.historyView.setGeometry(QtCore.QRect(10, 10, 461, 621))
        self.historyView.setObjectName("historyView")

        self.historyView.horizontalHeader().setStretchLastSection(True)

        # fill table by users data
        self.historyView.setModel(self.get_history_model())
        self.historyView.resizeColumnsToContents()
        self.historyView.resizeRowsToContents()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "History"))
