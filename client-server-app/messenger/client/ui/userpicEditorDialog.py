# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/templates/userpicEditor.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

from binascii import hexlify
from io import BytesIO
import os

from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from PyQt5 import QtCore, QtGui, QtWidgets


class UserpicEditorDialog(object):
    def __init__(self, client):
        super().__init__()

        self.client = client
        self.image = None
        self.cropped_image = None

        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def _draw_image(self, image, update_values=False):
        qt_image = ImageQt(image.convert("RGBA"))

        pixmap = QtGui.QPixmap.fromImage(qt_image)
        self.imageLabel.setPixmap(pixmap.scaled(250, 250))

        width, height = pixmap.width(), pixmap.height()
        if update_values:
            self.upperXEdit.setText("0")
            self.upperYEdit.setText("0")
            self.lowerXEdit.setText(str(width))
            self.lowerYEdit.setText(str(height))

        self.dialog.repaint()

    def showImageDialog(self):
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.dialog, "Open userpic image"
        )
        self.image = Image.open(image_path)
        self._draw_image(self.image, True)

    def cropImage(self):
        if not self.image:
            return

        upperX = self.upperXEdit.text()
        upperX = int(upperX) if upperX.isdigit() else 0
        upperY = self.upperYEdit.text()
        upperY = int(upperY) if upperY.isdigit() else 0

        width, height = self.image.size
        lowerX = self.lowerXEdit.text()
        lowerX = int(lowerX) if lowerX.isdigit() else width
        lowerY = self.lowerYEdit.text()
        lowerY = int(lowerY) if lowerY.isdigit() else height

        self.cropped_image = self.image.crop((upperX, upperY, lowerX, lowerY))
        self._draw_image(self.cropped_image)

    def saveImage(self):
        with BytesIO() as output:
            image = self.cropped_image or self.image
            if not image:
                return
            image = image.resize((30, 30), Image.BILINEAR)
            image.save(output, format="PNG")
            self.client._upload_userpic(hexlify(output.getvalue()).decode())

    def setupUi(self, userpicDialog):
        userpicDialog.setObjectName("userpicDialog")
        userpicDialog.resize(442, 271)
        self.imageLabel = QtWidgets.QLabel(userpicDialog)
        self.imageLabel.setGeometry(QtCore.QRect(20, 10, 250, 250))
        self.imageLabel.setAutoFillBackground(True)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")

        self.upperDescriptionLabel = QtWidgets.QLabel(userpicDialog)
        self.upperDescriptionLabel.setGeometry(QtCore.QRect(290, 10, 101, 16))
        self.upperDescriptionLabel.setObjectName("upperDescriptionLabel")

        self.upperOpenBracketLabel = QtWidgets.QLabel(userpicDialog)
        self.upperOpenBracketLabel.setGeometry(QtCore.QRect(310, 30, 21, 21))
        self.upperOpenBracketLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.upperOpenBracketLabel.setObjectName("upperOpenBracketLabel")
        self.upperSemicolonLabel = QtWidgets.QLabel(userpicDialog)
        self.upperSemicolonLabel.setGeometry(QtCore.QRect(360, 30, 21, 21))
        self.upperSemicolonLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.upperSemicolonLabel.setObjectName("upperSemicolonLabel")
        self.upperCloseBracketLabel = QtWidgets.QLabel(userpicDialog)
        self.upperCloseBracketLabel.setGeometry(QtCore.QRect(410, 30, 21, 21))
        self.upperCloseBracketLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.upperCloseBracketLabel.setObjectName("upperCloseBracketLabel")

        self.upperXEdit = QtWidgets.QLineEdit(userpicDialog)
        self.upperXEdit.setGeometry(QtCore.QRect(330, 30, 31, 21))
        self.upperXEdit.setObjectName("upperXEdit")
        self.upperYEdit = QtWidgets.QLineEdit(userpicDialog)
        self.upperYEdit.setGeometry(QtCore.QRect(380, 30, 31, 21))
        self.upperYEdit.setObjectName("upperYEdit")

        self.lowerDescriptionLabel = QtWidgets.QLabel(userpicDialog)
        self.lowerDescriptionLabel.setGeometry(QtCore.QRect(290, 80, 101, 16))
        self.lowerDescriptionLabel.setObjectName("lowerDescriptionLabel")

        self.loweOpenBracketLabel = QtWidgets.QLabel(userpicDialog)
        self.loweOpenBracketLabel.setGeometry(QtCore.QRect(310, 100, 21, 21))
        self.loweOpenBracketLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loweOpenBracketLabel.setObjectName("loweOpenBracketLabel")
        self.lowerSemicolonLabel = QtWidgets.QLabel(userpicDialog)
        self.lowerSemicolonLabel.setGeometry(QtCore.QRect(360, 100, 21, 21))
        self.lowerSemicolonLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lowerSemicolonLabel.setObjectName("lowerSemicolonLabel")
        self.lowerCloseBracketLabel = QtWidgets.QLabel(userpicDialog)
        self.lowerCloseBracketLabel.setGeometry(QtCore.QRect(410, 100, 21, 21))
        self.lowerCloseBracketLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lowerCloseBracketLabel.setObjectName("lowerCloseBracketLabel")

        self.lowerXEdit = QtWidgets.QLineEdit(userpicDialog)
        self.lowerXEdit.setGeometry(QtCore.QRect(330, 100, 31, 21))
        self.lowerXEdit.setObjectName("lowerXEdit")
        self.lowerYEdit = QtWidgets.QLineEdit(userpicDialog)
        self.lowerYEdit.setGeometry(QtCore.QRect(380, 100, 31, 21))
        self.lowerYEdit.setObjectName("lowerYEdit")

        self.cropButton = QtWidgets.QPushButton(userpicDialog)
        self.cropButton.setGeometry(QtCore.QRect(300, 140, 112, 32))
        self.cropButton.setObjectName("cropButton")
        self.cropButton.clicked.connect(self.cropImage)

        self.openButton = QtWidgets.QPushButton(userpicDialog)
        self.openButton.setGeometry(QtCore.QRect(300, 190, 112, 32))
        self.openButton.setObjectName("openButton")
        self.openButton.clicked.connect(self.showImageDialog)

        self.saveButton = QtWidgets.QPushButton(userpicDialog)
        self.saveButton.setGeometry(QtCore.QRect(300, 220, 112, 32))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.saveImage)

        self.retranslateUi(userpicDialog)
        QtCore.QMetaObject.connectSlotsByName(userpicDialog)

    def retranslateUi(self, userpicDialog):
        _translate = QtCore.QCoreApplication.translate
        userpicDialog.setWindowTitle(
            _translate("userpicDialog", "Userpic editor")
        )

        self.upperOpenBracketLabel.setText(_translate("userpicDialog", "("))
        self.upperSemicolonLabel.setText(_translate("userpicDialog", ";"))
        self.upperCloseBracketLabel.setText(_translate("userpicDialog", ")"))
        self.loweOpenBracketLabel.setText(_translate("userpicDialog", "("))
        self.lowerSemicolonLabel.setText(_translate("userpicDialog", ";"))
        self.lowerCloseBracketLabel.setText(_translate("userpicDialog", ")"))

        self.upperDescriptionLabel.setText(
            _translate("userpicDialog", "Upper left point")
        )
        self.lowerDescriptionLabel.setText(
            _translate("userpicDialog", "Lower right point")
        )
        self.cropButton.setText(_translate("userpicDialog", "Crop"))
        self.openButton.setText(_translate("userpicDialog", "Open"))
        self.saveButton.setText(_translate("userpicDialog", "Save"))
