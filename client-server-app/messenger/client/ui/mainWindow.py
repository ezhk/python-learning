# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/client/templates/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import sys

sys.path.append(".")

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from .addContactDialog import AddContactDialog
from .deleteContactDialog import DeleteContactDialog


class MainWindow(QtCore.QObject):
    def __init__(self, client=None):
        super().__init__()

        self.client = client

        self.window_object = QtWidgets.QMainWindow()
        self.message = QtWidgets.QMessageBox()

        # create window and show it
        self.setupUi(self.window_object)
        self.window_object.show()

    def bind_signals(self):
        self.client.client_error.connect(self.process_client_error)
        self.client.server_message.connect(self.process_server_message)

    @QtCore.pyqtSlot(str)
    def process_client_error(self, message):
        self.message.setWindowTitle("Connection error")
        self.message.setIcon(QtWidgets.QMessageBox.Warning)
        self.message.setText("Connection to server has been closed.")
        self.message.setDetailedText(message)

        self.message.exec()
        self.window_object.close()

    @QtCore.pyqtSlot(dict)
    def process_server_message(self, data):
        """
        Main function, that process messages from server.
        """

        def _process_contacts(self, contacts):
            self.contacts_model = QStandardItemModel()
            for contact in sorted(contacts):
                item = QStandardItem(contact)
                item.setEditable(False)
                self.contacts_model.appendRow(item)
            self.contactsView.setModel(self.contacts_model)

        def _process_chat(self, chat):
            self.chat_model = QStandardItemModel()
            for message in chat:
                item = QStandardItem(
                    f"{message['from']} > {message['to']} @ {message['ctime']}:\n{message['text']}"
                )
                item.setEditable(False)
                self.chat_model.appendRow(item)
            self.chatView.setModel(self.chat_model)

        if data.get("action", "") == "update_contacts":
            _process_contacts(self, self.client.contacts)
        if data.get("action", "") == "update_chat":
            _process_chat(self, self.client.chat)

    def send_message(self):
        text = self.messageEdit.toPlainText()
        if not self.client.active_chat or not text:
            return
        self.client._send_message(self.client.active_chat, text)

        # fix clean area
        self.messageEdit.clear()
        self.client._get_chat(self.client.active_chat)

    def add_contact(self):
        AddContactDialog(self.client)

    def remove_contact(self):
        DeleteContactDialog(self.client)

    def select_contact_user(self):
        # clean chat view and enable Send button
        self.chatView.setModel(QStandardItemModel())
        self.messageEdit.setEnabled(True)

        self.client.active_chat = self.contactsView.currentIndex().data()
        self.chatLabel.setText(f"Chat with {self.client.active_chat}")

        self.client._get_chat(self.client.active_chat)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 630)

        self.exitMenu = QtWidgets.QAction("Exit", MainWindow)
        self.exitMenu.triggered.connect(QtWidgets.qApp.exit)
        self.toolbar = MainWindow.addToolBar("ToolBar")
        self.toolbar.addAction(self.exitMenu)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.contactsLabel = QtWidgets.QLabel(self.centralwidget)
        self.contactsLabel.setGeometry(QtCore.QRect(20, 10, 59, 16))
        self.contactsLabel.setObjectName("contactsLabel")
        self.contactsView = QtWidgets.QListView(self.centralwidget)
        self.contactsView.setGeometry(QtCore.QRect(10, 30, 231, 521))
        self.contactsView.setObjectName("contactsView")
        self.contactsView.doubleClicked.connect(self.select_contact_user)

        self.addContactButton = QtWidgets.QPushButton(self.centralwidget)
        self.addContactButton.setGeometry(QtCore.QRect(10, 560, 113, 41))
        self.addContactButton.setObjectName("addContactButton")
        self.addContactButton.clicked.connect(self.add_contact)

        self.removeContactButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeContactButton.setGeometry(QtCore.QRect(130, 560, 113, 41))
        self.removeContactButton.setObjectName("removeContactButton")
        self.removeContactButton.clicked.connect(self.remove_contact)

        self.chatLabel = QtWidgets.QLabel(self.centralwidget)
        self.chatLabel.setGeometry(QtCore.QRect(290, 10, 250, 16))
        self.chatLabel.setObjectName("chatLabel")
        self.chatView = QtWidgets.QListView(self.centralwidget)
        self.chatView.setGeometry(QtCore.QRect(280, 30, 521, 371))
        self.chatView.setObjectName("chatView")

        self.messageLabel = QtWidgets.QLabel(self.centralwidget)
        self.messageLabel.setGeometry(QtCore.QRect(290, 420, 61, 16))
        self.messageLabel.setObjectName("messageLabel")
        self.messageEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.messageEdit.setGeometry(QtCore.QRect(280, 440, 521, 111))
        self.messageEdit.setObjectName("messageEdit")
        self.messageEdit.setEnabled(False)

        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(690, 560, 113, 41))
        self.sendButton.setObjectName("sendButton")
        self.sendButton.clicked.connect(self.send_message)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Client"))
        self.contactsLabel.setText(_translate("MainWindow", "Contacts"))
        self.addContactButton.setText(_translate("MainWindow", "Add"))
        self.removeContactButton.setText(_translate("MainWindow", "Remove"))
        self.sendButton.setText(_translate("MainWindow", "Send"))
        self.chatLabel.setText(_translate("MainWindow", "Chat"))
        self.messageLabel.setText(_translate("MainWindow", "Message"))
