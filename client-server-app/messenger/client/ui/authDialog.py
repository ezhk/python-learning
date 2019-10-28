# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/client/templates/autorizeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class AuthDialog(object):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None

        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.show()

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def authorization_action(self):
        self.username = self.usernameEdit.text()
        self.password = self.passwordEdit.text()
        if self.username and self.password:
            return self.dialog.close()

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Sign in failed")
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Username and password cannot be empty")
        msg.exec()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 125)
        self.labelUsername = QtWidgets.QLabel(Dialog)
        self.labelUsername.setGeometry(QtCore.QRect(40, 20, 61, 16))
        self.labelUsername.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.labelUsername.setObjectName("labelUsername")

        self.usernameEdit = QtWidgets.QLineEdit(Dialog)
        self.usernameEdit.setGeometry(QtCore.QRect(130, 20, 181, 21))
        self.usernameEdit.setObjectName("usernameEdit")

        self.labelPassowrd = QtWidgets.QLabel(Dialog)
        self.labelPassowrd.setGeometry(QtCore.QRect(40, 50, 61, 16))
        self.labelPassowrd.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.labelPassowrd.setObjectName("labelPassowrd")

        self.passwordEdit = QtWidgets.QLineEdit(Dialog)
        self.passwordEdit.setGeometry(QtCore.QRect(130, 50, 181, 21))
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")

        self.loginButton = QtWidgets.QPushButton(Dialog)
        self.loginButton.setGeometry(QtCore.QRect(50, 80, 113, 32))
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(self.authorization_action)

        self.exitButton = QtWidgets.QPushButton(Dialog)
        self.exitButton.setGeometry(QtCore.QRect(190, 80, 111, 32))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(QtWidgets.qApp.quit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Authorize"))
        self.labelUsername.setText(_translate("Dialog", "Username"))
        self.labelPassowrd.setText(_translate("Dialog", "Password"))
        self.loginButton.setText(_translate("Dialog", "Login"))
        self.exitButton.setText(_translate("Dialog", "Exit"))
