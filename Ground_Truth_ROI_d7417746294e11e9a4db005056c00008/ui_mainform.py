# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainform.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(454, 219)
        self.verticalLayout = QtWidgets.QVBoxLayout(MainForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(MainForm)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(MainForm)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_ROI1 = QtWidgets.QLabel(MainForm)
        self.label_ROI1.setObjectName("label_ROI1")
        self.horizontalLayout_2.addWidget(self.label_ROI1)
        self.comboBox_ROI1 = OrsObjectClassComboBox(MainForm)
        self.comboBox_ROI1.setObjectName("comboBox_ROI1")
        self.horizontalLayout_2.addWidget(self.comboBox_ROI1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_ROI2 = QtWidgets.QLabel(MainForm)
        self.label_ROI2.setObjectName("label_ROI2")
        self.horizontalLayout.addWidget(self.label_ROI2)
        self.comboBox_ROI2 = OrsObjectClassComboBox(MainForm)
        self.comboBox_ROI2.setObjectName("comboBox_ROI2")
        self.horizontalLayout.addWidget(self.comboBox_ROI2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_ROI1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ROI1.setObjectName("horizontalLayout_ROI1")
        self.label_ROI3 = QtWidgets.QLabel(MainForm)
        self.label_ROI3.setObjectName("label_ROI3")
        self.horizontalLayout_ROI1.addWidget(self.label_ROI3)
        self.comboBox_ROI3 = OrsObjectClassComboBox(MainForm)
        self.comboBox_ROI3.setObjectName("comboBox_ROI3")
        self.horizontalLayout_ROI1.addWidget(self.comboBox_ROI3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_ROI1)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_4 = QtWidgets.QLabel(MainForm)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.lineEdit_GroundTruthName = QtWidgets.QLineEdit(MainForm)
        self.lineEdit_GroundTruthName.setObjectName("lineEdit_GroundTruthName")
        self.horizontalLayout_3.addWidget(self.lineEdit_GroundTruthName)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.pushButton_Compute = QtWidgets.QPushButton(MainForm)
        self.pushButton_Compute.setObjectName("pushButton_Compute")
        self.verticalLayout_4.addWidget(self.pushButton_Compute)
        self.label_3 = QtWidgets.QLabel(MainForm)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Form"))
        self.label.setText(_translate("MainForm", "Create a Ground Truth ROI that is the average of 3 seperate ROIS:"))
        self.label_2.setText(_translate("MainForm", "Select the Three ROIS:"))
        self.label_ROI1.setText(_translate("MainForm", "ROI 1:"))
        self.label_ROI2.setText(_translate("MainForm", "ROI 2:"))
        self.label_ROI3.setText(_translate("MainForm", "ROI 3: "))
        self.label_4.setText(_translate("MainForm", "Name of Ground Truth ROI:                             "))
        self.lineEdit_GroundTruthName.setText(_translate("MainForm", "Ground_Truth_ROI"))
        self.pushButton_Compute.setText(_translate("MainForm", "Compute"))

from ORSServiceClass.ORSWidget.orsobjectclasscombobox.orsobjectclasscombobox import OrsObjectClassComboBox

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QWidget()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec_())

