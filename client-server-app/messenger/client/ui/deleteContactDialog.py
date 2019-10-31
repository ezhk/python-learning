# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/client/templates/deleteContactDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class DeleteContactDialog(object):
    def __init__(self, client=None):
        super().__init__()

        self.client = client

        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def _delete_contact(self):
        self.client._delete_contact(self.usernameBox.currentText())
        return self.client._get_contacts()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(329, 104)
        self.usernameLabel = QtWidgets.QLabel(Dialog)
        self.usernameLabel.setGeometry(QtCore.QRect(40, 20, 71, 16))
        self.usernameLabel.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.usernameLabel.setObjectName("usernameLabel")

        self.usernameBox = QtWidgets.QComboBox(Dialog)
        self.usernameBox.setGeometry(QtCore.QRect(130, 21, 161, 21))
        self.usernameBox.setObjectName("usernameBox")
        self.usernameBox.addItems(self.client.contacts)

        self.deleteButton = QtWidgets.QPushButton(Dialog)
        self.deleteButton.setGeometry(QtCore.QRect(40, 60, 113, 32))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self._delete_contact)

        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(180, 60, 113, 32))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.dialog.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Delete contanct"))
        self.usernameLabel.setText(_translate("Dialog", "Username"))
        self.deleteButton.setText(_translate("Dialog", "Delete"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
