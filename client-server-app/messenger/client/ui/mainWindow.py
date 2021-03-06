# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/client/templates/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

from binascii import unhexlify
from io import BytesIO
import sys

sys.path.append(".")

from PIL import Image
from PIL.ImageQt import ImageQt

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QIcon,
    QFont,
    QPixmap,
)

from .userpicEditorDialog import UserpicEditorDialog
from .addContactDialog import AddContactDialog
from .deleteContactDialog import DeleteContactDialog
from .imageEditorDialog import ImageEditorDialog


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

    def process_background(self, sender, message):
        self.message.setWindowTitle("Received message")
        self.message.setIcon(QtWidgets.QMessageBox.Information)
        self.message.setText(f"New message from {sender.capitalize()}")
        self.message.setDetailedText(message)
        self.message.exec()

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

        def _process_profile(self, profile):
            if profile is None:
                return
            self.usernameLabel.setText(
                profile.get("username", "anonimous").capitalize()
            )

            if profile.get("userpic", None) is None:
                image = Image.open("ui/images/userpic.png")
                image = image.resize((30, 30), Image.BILINEAR)
            else:
                raw_image = unhexlify(profile.get("userpic").encode())
                stream = BytesIO(raw_image)
                image = Image.open(stream)

            qt_image = ImageQt(image.convert("RGBA"))
            pixmap = QPixmap.fromImage(qt_image)
            self.userpicLabel.setPixmap(pixmap)

        def _process_backgroud_message(self, sender, message):
            self.process_background(sender, message)

        if data.get("action", "") == "update_contacts":
            _process_contacts(self, self.client.contacts)
        if data.get("action", "") == "update_chat":
            _process_chat(self, self.client.chat)
        if data.get("action", "") == "update_profile":
            _process_profile(self, self.client.user_profile)
        if data.get("action", "") == "background_message":
            _process_backgroud_message(
                self, data.get("from"), data.get("message")
            )

    def send_message(self):
        text = self.messageEdit.toPlainText()
        if not self.client.active_chat or not text:
            return
        self.client._send_message(self.client.active_chat, text)

        # fix clean area
        self.messageEdit.clear()
        self.messageEdit.repaint()
        self.client._get_chat(self.client.active_chat)

    def update_userpic(self, event):
        UserpicEditorDialog(self.client)

    def add_contact(self):
        AddContactDialog(self.client)

    def remove_contact(self):
        DeleteContactDialog(self.client)

    def add_file(self):
        ImageEditorDialog()

    def select_contact_user(self):
        # clean chat view and enable Send button
        self.chatView.setModel(QStandardItemModel())
        self.messageEdit.setEnabled(True)

        self.client.active_chat = self.contactsView.currentIndex().data()
        self.chatLabel.setText(f"Chat with {self.client.active_chat}")

        self.client._get_chat(self.client.active_chat)

    def set_text(self, font_type):
        font = QFont()

        if font_type == "bold":
            font.setBold(True)
        elif font_type == "italic":
            font.setItalic(True)
        elif font_type == "undelined":
            font.setUnderline(True)

        self.messageEdit.setFont(font)
        self.messageEdit.repaint()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 630)

        self.exitMenu = QtWidgets.QAction("Exit", MainWindow)
        self.exitMenu.triggered.connect(QtWidgets.qApp.exit)
        self.toolbar = MainWindow.addToolBar("ToolBar")
        self.toolbar.setMovable(False)
        self.toolbar.addAction(self.exitMenu)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.userpicLabel = QtWidgets.QLabel(self.centralwidget)
        self.userpicLabel.setGeometry(QtCore.QRect(20, 5, 30, 30))
        self.userpicLabel.setObjectName("userpicLabel")
        self.userpicLabel.mousePressEvent = self.update_userpic

        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setGeometry(QtCore.QRect(60, 10, 181, 21))
        self.usernameLabel.setText("Anonimous")
        self.usernameLabel.setObjectName("usernameLabel")

        self.contactsLabel = QtWidgets.QLabel(self.centralwidget)
        self.contactsLabel.setGeometry(QtCore.QRect(10, 40, 59, 16))
        self.contactsLabel.setObjectName("contactsLabel")
        self.contactsView = QtWidgets.QListView(self.centralwidget)
        self.contactsView.setGeometry(QtCore.QRect(10, 60, 231, 491))
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

        self.addFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.addFileButton.setGeometry(QtCore.QRect(280, 560, 36, 32))
        self.addFileButton.setObjectName("addFileButton")
        self.addFileButton.clicked.connect(self.add_file)

        self.undelinedButton = QtWidgets.QPushButton(self.centralwidget)
        self.undelinedButton.setGeometry(QtCore.QRect(320, 560, 31, 32))
        self.undelinedButton.setObjectName("undelinedButton")
        self.undelinedButton.clicked.connect(
            lambda: self.set_text("undelined")
        )
        self.italicButton = QtWidgets.QPushButton(self.centralwidget)
        self.italicButton.setGeometry(QtCore.QRect(350, 560, 31, 32))
        self.italicButton.setObjectName("italicButton")
        self.italicButton.clicked.connect(lambda: self.set_text("italic"))
        self.boldButton = QtWidgets.QPushButton(self.centralwidget)
        self.boldButton.setGeometry(QtCore.QRect(380, 560, 31, 32))
        self.boldButton.setObjectName("boldButton")
        self.boldButton.clicked.connect(lambda: self.set_text("bold"))

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

        username_font = QFont()
        username_font.setPointSize(15)
        username_font.setBold(True)
        self.usernameLabel.setFont(username_font)

        self.contactsLabel.setText(_translate("MainWindow", "Contacts"))
        self.addContactButton.setText(_translate("MainWindow", "Add"))
        self.removeContactButton.setText(_translate("MainWindow", "Remove"))

        self.addFileButton.setText(_translate("MainWindow", "\U0001F4F7"))

        self.undelinedButton.setText(_translate("MainWindow", "U"))
        underline_font = QFont()
        underline_font.setUnderline(True)
        self.undelinedButton.setFont(underline_font)

        self.italicButton.setText(_translate("MainWindow", "I"))
        self.italicButton.setFont(QFont("monospace", italic=True))
        self.boldButton.setText(_translate("MainWindow", "B"))
        self.boldButton.setFont(QFont("monospace", weight=QFont.Bold))

        self.sendButton.setText(_translate("MainWindow", "Send"))

        self.chatLabel.setText(_translate("MainWindow", "Chat"))
        self.messageLabel.setText(_translate("MainWindow", "Message"))
