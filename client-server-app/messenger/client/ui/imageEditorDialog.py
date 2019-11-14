# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/templates/imageEditor.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

from PyQt5 import QtCore, QtGui, QtWidgets


class ImageEditorDialog(object):
    def __init__(self):
        super().__init__()
        self.image_path = None

        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def showFileDialog(self):
        self.image_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.dialog, "Open image"
        )
        pixmap = QtGui.QPixmap(self.image_path)
        # self.imageLabel.resize(300, 300)
        self.imageLabel.setPixmap(pixmap)

    def convert_image(self, filter_name=None):
        def _filter_sephia(r, g, b):
            depth = 30

            S = r + g + b
            r = S + depth * 2
            g = S + depth
            b = S
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255
            return r, g, b

        def _filter_bw(r, g, b):
            factor = 50

            S = r + g + b
            if S > (((255 + factor) // 2) * 3):
                return 255, 255, 255
            return 0, 0, 0

        def _filter_grayscale(r, g, b):
            S = (r + g + b) // 3
            return S, S, S

        def _filter_negative(r, g, b):
            return 255 - r, 255 - g, 255 - b

        if not self.image_path:
            return None

        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size
        pix = image.load()

        for i in range(width):
            for j in range(height):
                r, g, b = pix[i, j][:3]
                r, g, b = locals().get(f"_filter_{filter_name}")(r, g, b)
                draw.point((i, j), (r, g, b))

        tmp_image = ImageQt(image.convert("RGBA"))
        pixmap = QtGui.QPixmap.fromImage(tmp_image)
        self.imageLabel.setPixmap(pixmap)
        self.dialog.repaint()

    def setupUi(self, imageEditor):
        imageEditor.setObjectName("imageEditor")
        imageEditor.resize(488, 546)
        self.label = QtWidgets.QLabel(imageEditor)
        self.label.setGeometry(QtCore.QRect(200, 10, 81, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.imageLabel = QtWidgets.QLabel(imageEditor)
        self.imageLabel.setGeometry(QtCore.QRect(20, 40, 441, 411))
        self.imageLabel.setAutoFillBackground(True)
        self.imageLabel.setText("")
        self.imageLabel.setScaledContents(False)
        self.imageLabel.setWordWrap(False)
        self.imageLabel.setObjectName("imageLabel")

        self.openImageButton = QtWidgets.QPushButton(imageEditor)
        self.openImageButton.setGeometry(QtCore.QRect(180, 460, 121, 31))
        self.openImageButton.setObjectName("openImageButton")
        self.openImageButton.clicked.connect(self.showFileDialog)

        self.sephiaButton = QtWidgets.QPushButton(imageEditor)
        self.sephiaButton.setGeometry(QtCore.QRect(30, 500, 91, 32))
        self.sephiaButton.setObjectName("sephiaButton")
        self.sephiaButton.clicked.connect(lambda: self.convert_image("sephia"))

        self.bwButton = QtWidgets.QPushButton(imageEditor)
        self.bwButton.setGeometry(QtCore.QRect(140, 500, 91, 32))
        self.bwButton.setObjectName("bwButton")
        self.bwButton.clicked.connect(lambda: self.convert_image("bw"))

        self.grayscaleButton = QtWidgets.QPushButton(imageEditor)
        self.grayscaleButton.setGeometry(QtCore.QRect(250, 500, 91, 32))
        self.grayscaleButton.setObjectName("grayscaleButton")
        self.grayscaleButton.clicked.connect(
            lambda: self.convert_image("grayscale")
        )

        self.negativeButton = QtWidgets.QPushButton(imageEditor)
        self.negativeButton.setGeometry(QtCore.QRect(360, 500, 91, 32))
        self.negativeButton.setObjectName("negativeButton")
        self.negativeButton.clicked.connect(
            lambda: self.convert_image("negative")
        )

        self.retranslateUi(imageEditor)
        QtCore.QMetaObject.connectSlotsByName(imageEditor)

    def retranslateUi(self, imageEditor):
        _translate = QtCore.QCoreApplication.translate
        imageEditor.setWindowTitle(_translate("imageEditor", "Dialog"))
        self.label.setText(_translate("imageEditor", "Image editor"))
        self.openImageButton.setText(_translate("imageEditor", "Open image"))
        self.sephiaButton.setText(_translate("imageEditor", "Sephia"))
        self.bwButton.setText(_translate("imageEditor", "B/W"))
        self.grayscaleButton.setText(_translate("imageEditor", "Grayscale"))
        self.negativeButton.setText(_translate("imageEditor", "Negative"))
