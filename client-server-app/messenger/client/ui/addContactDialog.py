# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/client/templates/addContactDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class AddContactDialog(object):
    def __init__(self, client=None):
        super().__init__()

        self.client = client

        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def _add_contact(self):
        self.client._add_contact(self.lineEdit.text())
        return self.client._get_contacts()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(329, 104)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 71, 16))
        self.label.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(140, 20, 141, 21))
        self.lineEdit.setObjectName("lineEdit")

        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setGeometry(QtCore.QRect(40, 60, 113, 32))
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self._add_contact)

        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(170, 60, 113, 32))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.dialog.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add contanct"))
        self.label.setText(_translate("Dialog", "Username"))
        self.addButton.setText(_translate("Dialog", "Add"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
