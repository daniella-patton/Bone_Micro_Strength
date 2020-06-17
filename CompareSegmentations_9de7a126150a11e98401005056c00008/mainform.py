from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from ORSModel import ROI

from OrsLibraries.workingcontext import WorkingContext
from ORSServiceClass.windowclasses.orsabstractwindow import OrsAbstractWindow
from .ui_mainform import Ui_MainForm


class MainForm(OrsAbstractWindow):

    def __init__(self, implementation, parent=None):
        super().__init__(implementation, parent)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        WorkingContext.registerOrsWidget('CompareSegmentations_9de7a126150a11e98401005056c00008', self.getImplementation(), 'MainForm', self)

        self.ui.comboBox_GoldStandardROI.setManagedClass(ROI)
        self.ui.comboBox_ROItoCompare.setManagedClass(ROI)

    def closeEvent(self, event):
        self.getImplementation().deletePlugin(self)
        event.accept()

    def updateLineEditTriggersCount(self):
        newValueAsInt = self.getImplementation().getTriggersCount()
        newValueAsString = str(newValueAsInt)
        self.ui.lineEdit_triggersCount.setText(newValueAsString)



    @pyqtSlot(bool)
    def on_toolButton_OpenFileBrowser_clicked(self, checked):

        selectedFileName, filter_ = QFileDialog.getSaveFileName(caption="Select a File", directory=self.ui.lineEdit_FileName.text())

        if selectedFileName == '':
            return

        self.ui.lineEdit_FileName.setText(selectedFileName)

    @pyqtSlot(bool)
    def on_pushButton_Compare_clicked(self, checked):
        goldStandardROI = self.ui.comboBox_GoldStandardROI.getSelectedObject()
        aROIToCompare = self.ui.comboBox_ROItoCompare.getSelectedObject()
        filename = self.ui.lineEdit_FileName.text()

        #  Call function to compute the comparison statistics
        self.getImplementation().compareSegmentations(goldStandardROI, aROIToCompare, filename)

        # Update the fields in GUI with the calculated properties
        self.ui.lineEdit_valueTP.setText(str(self.getImplementation().getValueTP()))
        self.ui.lineEdit_valueFP.setText(str(self.getImplementation().getValueFP()))
        self.ui.lineEdit_valueTN.setText(str(self.getImplementation().getValueTN()))
        self.ui.lineEdit_valueFN.setText(str(self.getImplementation().getValueFN()))
        self.ui.lineEdit_valueDSC.setText(str(self.getImplementation().getValueDSC()))
        self.ui.lineEdit_valueVS.setText(str(self.getImplementation().getValueVS()))
        self.ui.lineEdit_valueRI.setText(str(self.getImplementation().getValueRI()))
        self.ui.lineEdit_valueKAP.setText(str(self.getImplementation().getValueKAP()))
        self.ui.lineEdit_valueAVD.setText(str(self.getImplementation().getValueAVD()))
        self.ui.lineEdit_valueTPR.setText(str(self.getImplementation().getValueTPR()))
