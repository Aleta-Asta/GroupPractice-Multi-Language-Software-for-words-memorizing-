# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tiankong.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fanyi(object):
    def setupUi(self, fanyi):
        fanyi.setObjectName("fanyi")
        fanyi.resize(745, 678)
        self.PrimaryPushButton = PrimaryPushButton(fanyi)
        self.PrimaryPushButton.setGeometry(QtCore.QRect(280, 580, 211, 51))
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.CaptionLabel = CaptionLabel(fanyi)
        self.CaptionLabel.setGeometry(QtCore.QRect(110, 190, 541, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.CaptionLabel.setFont(font)
        self.CaptionLabel.setWordWrap(True)
        self.CaptionLabel.setObjectName("CaptionLabel")
        self.layoutWidget = QtWidgets.QWidget(fanyi)
        self.layoutWidget.setGeometry(QtCore.QRect(110, 350, 561, 201))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.xuanxiangA = CheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.xuanxiangA.setFont(font)
        self.xuanxiangA.setObjectName("xuanxiangA")
        self.verticalLayout.addWidget(self.xuanxiangA)
        self.xuanxiangB = CheckBox(self.layoutWidget)
        self.xuanxiangB.setObjectName("xuanxiangB")
        self.verticalLayout.addWidget(self.xuanxiangB)
        self.xuanxiangC = CheckBox(self.layoutWidget)
        self.xuanxiangC.setObjectName("xuanxiangC")
        self.verticalLayout.addWidget(self.xuanxiangC)
        self.xuanxaingD = CheckBox(self.layoutWidget)
        self.xuanxaingD.setObjectName("xuanxaingD")
        self.verticalLayout.addWidget(self.xuanxaingD)
        self.HyperlinkButton = HyperlinkButton(fanyi)
        self.HyperlinkButton.setGeometry(QtCore.QRect(30, 90, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.HyperlinkButton.setFont(font)
        self.HyperlinkButton.setCheckable(False)
        self.HyperlinkButton.setObjectName("HyperlinkButton")
        self.ProgressBar = ProgressBar(fanyi)
        self.ProgressBar.setGeometry(QtCore.QRect(100, 30, 521, 4))
        self.ProgressBar.setProperty("value", 75)
        self.ProgressBar.setVal(75.0)
        self.ProgressBar.setObjectName("ProgressBar")
        self.ProgressRing = ProgressRing(fanyi)
        self.ProgressRing.setGeometry(QtCore.QRect(520, 80, 100, 100))
        self.ProgressRing.setProperty("value", 75)
        self.ProgressRing.setVal(75.0)
        self.ProgressRing.setObjectName("ProgressRing")
        self.HyperlinkLabel = HyperlinkLabel(fanyi)
        self.HyperlinkLabel.setGeometry(QtCore.QRect(557, 113, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.HyperlinkLabel.setFont(font)
        self.HyperlinkLabel.setObjectName("HyperlinkLabel")

        self.retranslateUi(fanyi)
        QtCore.QMetaObject.connectSlotsByName(fanyi)

    def retranslateUi(self, fanyi):
        _translate = QtCore.QCoreApplication.translate
        fanyi.setWindowTitle(_translate("fanyi", "Form"))
        self.PrimaryPushButton.setText(_translate("fanyi", "Primary push button"))
        self.CaptionLabel.setText(_translate("fanyi", "Here is a sample question. Select the most appropriate option from the choices to fill in the blank.Here is a sample question. Select the most appropriate option from the choices to fill in the blank.  "))
        self.xuanxiangA.setText(_translate("fanyi", "Check box"))
        self.xuanxiangB.setText(_translate("fanyi", "Check box"))
        self.xuanxiangC.setText(_translate("fanyi", "Check box"))
        self.xuanxaingD.setText(_translate("fanyi", "Check box"))
        self.HyperlinkButton.setText(_translate("fanyi", "word"))
        self.HyperlinkLabel.setText(_translate("fanyi", "acc"))
from qfluentwidgets import CaptionLabel, CheckBox, HyperlinkButton, HyperlinkLabel, PrimaryPushButton, ProgressBar, ProgressRing
