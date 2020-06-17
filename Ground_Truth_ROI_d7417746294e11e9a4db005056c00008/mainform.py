from PyQt5.QtCore import pyqtSlot
from ORSModel import ROI

from OrsLibraries.workingcontext import WorkingContext
from ORSServiceClass.windowclasses.orsabstractwindow import OrsAbstractWindow
from .ui_mainform import Ui_MainForm


class MainForm(OrsAbstractWindow):

    def __init__(self, implementation, parent=None):
        super().__init__(implementation, parent)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        WorkingContext.registerOrsWidget('Ground_Truth_ROI_d7417746294e11e9a4db005056c00008', self.getImplementation(), 'MainForm', self)
        self.ui.comboBox_ROI1.setManagedClass(ROI)
        self.ui.comboBox_ROI2.setManagedClass(ROI)
        self.ui.comboBox_ROI3.setManagedClass(ROI)

    def closeEvent(self, event):
        self.getImplementation().deletePlugin(self)
        event.accept()


    @pyqtSlot(bool)
    def on_pushButton_Compute_clicked(self, checked):
        aROI1 = self.ui.comboBox_ROI1.getSelectedObject()
        aROI2 = self.ui.comboBox_ROI2.getSelectedObject()
        aROI3 = self.ui.comboBox_ROI3.getSelectedObject()
        aGTName = self.ui.lineEdit_GroundTruthName.text()
        print('selected the ROIs and the aGTName: ', str(aGTName))
        self.getImplementation().GroundTruthROI(aROI1, aROI2, aROI3, aGTName)

