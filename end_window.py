# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'end_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EndWindow(object):
    def setupUi(self, EndWindow):
        EndWindow.setObjectName("EndWindow")
        EndWindow.resize(448, 300)
        EndWindow.setMinimumSize(QtCore.QSize(448, 300))
        EndWindow.setMaximumSize(QtCore.QSize(448, 300))
        font = QtGui.QFont()
        font.setPointSize(14)
        EndWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(EndWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(310, 30, 130, 30))
        self.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(310, 120, 130, 30))
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(310, 150, 130, 30))
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(119, 240, 210, 40))
        self.pushButton.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 300, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 300, 30))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 150, 300, 30))
        self.label_3.setObjectName("label_3")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 80, 430, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(10, 200, 430, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        EndWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EndWindow)
        QtCore.QMetaObject.connectSlotsByName(EndWindow)

    def retranslateUi(self, EndWindow):
        _translate = QtCore.QCoreApplication.translate
        EndWindow.setWindowTitle(_translate("EndWindow", "Европейский опцион"))
        self.pushButton.setText(_translate("EndWindow", "ОK"))
        self.label.setText(_translate("EndWindow", "<html><head/><body><p align=\"center\">Функция выплаты равна</p></body></html>"))
        self.label_2.setText(_translate("EndWindow", "<html><head/><body><p align=\"center\">Долг банку</p></body></html>"))
        self.label_3.setText(_translate("EndWindow", "<html><head/><body><p align=\"center\">Выплата покупателю</p></body></html>"))

