from OrsLibraries.workingcontext import WorkingContext
from ORSServiceClass.windowclasses.orsabstractwindow import OrsAbstractWindow
from .ui_mainform import Ui_MainForm
from ORSModel import ROI
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog

class MainForm(OrsAbstractWindow):

    def __init__(self, implementation, parent=None):
        super().__init__(implementation, parent)
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        WorkingContext.registerOrsWidget('BoneQuadrentAnalysis_6be3f97a40e711e9ae07005056c00008', self.getImplementation(), 'MainForm', self)
        self.ui.BoneROIcomboBox.setManagedClass(ROI)
        self.ui.CorticalROIcomboBox.setManagedClass(ROI)
        self.ui.MarrowROIcomboBox.setManagedClass(ROI)

    def closeEvent(self, event):
        self.getImplementation().deletePlugin(self)
        event.accept()

    @pyqtSlot(bool)
    def on_toolButton_OutputFolder_clicked(self, checked):

        selectedFolderName = QFileDialog.getExistingDirectory(caption="Select a Folder", directory=self.ui.OutputFolderlineEdit.text())

        print('Selected file name: ', selectedFolderName)

        if selectedFolderName == '':
            return

        self.ui.OutputFolderlineEdit.setText(selectedFolderName)

    @pyqtSlot(bool)
    def on_ComputepushButton_clicked(self, checked):
        boneROI = self.ui.BoneROIcomboBox.getSelectedObject()
        corticalROI = self.ui.CorticalROIcomboBox.getSelectedObject()
        marrowROI = self.ui.MarrowROIcomboBox.getSelectedObject()
        foldername = self.ui.OutputFolderlineEdit.text()
        # bCalcMarrow = True
        # bCalcMarrow = False
        bCalcMarrow = self.ui.checkBox_calcMarrowProps.isChecked()
        bCalcCorticalSlice = self.ui.checkBox_calcCorticalSliceProps.isChecked()
        bCalc3DQuad = self.ui.checkBox_calcBoneQuadrentProps.isChecked()
        zslicePadding = self.ui.zSlicePadding_spinBox.value()

        print(' The ROIs and foldername have been loaded... ', foldername)
        print('  Calling BoneQuadrentAnalysis...')
        #  Call function to compute regional cortical and trabecular anlaysis
        self.getImplementation().BoneQuadrentAnalysis(boneROI, corticalROI, marrowROI, foldername, bCalcMarrow,
                                                      bCalcCorticalSlice, bCalc3DQuad, zslicePadding)

        print(' ')
        print('     Finished Bone Quadrent Analysis....')
        print(' ')

