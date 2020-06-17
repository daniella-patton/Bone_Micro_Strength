"""
This plugin is used to compare two ROIs, calculating various statistical
measures to quantify the differences (similarity).

The measures currently being calculated are:
    DICE
    Volumetric Similarity (VS)
    Rand Index (RI)
    Cohen Kappa Coefficient (KAPA)
Others may be added in the future.

:author: Daniella Patton & Rob Goulet
:contact: 
:email: pattondm@umich.edu; rgoulet@med.umich.edu
:organization: Orthopeadic Research Labs, University of Michigan
:address: 109 Zina Pitcher Place, Rm. 2001, Ann Arbor, MI, 48109
:copyright: 2019
:date: Jan 23 2019 10:47
:dragonflyVersion: 4.0.0.554
:UUID: 9de7a126150a11e98401005056c00008
"""

__version__ = '1.0.0'

from OrsLibraries.workingcontext import WorkingContext
from ORSServiceClass.OrsPlugin.orsPlugin import OrsPlugin
from ORSServiceClass.decorators.infrastructure import menuItem
from ORSServiceClass.decorators.infrastructure import interfaceMethod
from ORSServiceClass.actionAndMenu.menu import Menu
from ORSServiceClass.OrsPlugin.uidescriptor import UIDescriptor
from ORSModel.ors import StructuredGrid, ROI
from ORSModel import ROI, Channel
from OrsHelpers.roihelper import ROIHelper
from .mainform import MainForm
import numpy as np
from scipy.spatial.distance import directed_hausdorff


class CompareSegmentations_9de7a126150a11e98401005056c00008(OrsPlugin):

    # Plugin definition
    multiple = False
    closable = True
    savable = False
    keepAlive = False

    # UIs
    UIDescriptors = [UIDescriptor(name='MainForm',
                                  title='Compare Segmentations',
                                  dock='Floating',
                                  tab='Main',
                                  modal=False,
                                  collapsible=True,
                                  movable=True,
                                  floatable=True)]

    def __init__(self, varname=None, managed=True):
        super().__init__(varname, managed)

    def openWidget(self, name, dock=None, tab=None, x=-1, y=-1, w=-1, l=-1, order=-1):
        form = self.getFormNamed(name)
        if form is not None:
            form.show()
            form.raise_()
            form.activateWindow()
            return
        if name == self.getMainFormName():
            _orsParent = WorkingContext.getCurrentContextWindow()
            form = MainForm(implementation=self, parent=_orsParent)
            self.setFormNamed(name, form)
            WorkingContext.addOrsWidget(self.obj, name, form, dock, tab, x, y, w, l, order)

    def closeWidget(self, name):
        self.closeFormNamed(name)

    @classmethod
    def openGUI(cls):
        instance = CompareSegmentations_9de7a126150a11e98401005056c00008()
        if instance is not None:
            instance.openWidget('MainForm')

    @classmethod
    @menuItem('ORL')
    def menuItemStartPlugin(cls):
        aMenuItem = Menu(title='Compare Segmentations',
                         id_='CompareSegmentations_9de7a126150a11e98401005056c00008_1',
                         section='',
                         action='CompareSegmentations_9de7a126150a11e98401005056c00008.openGUI()')
        return aMenuItem

    def getValueTP(cls):
        return cls._valueTP

    def getValueFP(cls):
        return cls._valueFP

    def getValueTN(cls):
        return cls._valueTN

    def getValueFN(cls):
        return cls._valueFN

    def getValueDSC(cls):
        return cls._valueDSC

    def getValueVS(cls):
        return cls._valueVS

    def getValueRI(cls):
        return cls._valueRI

    def getValueKAP(cls):
        return cls._valueKAP

    def getValueAVD(cls):
        return cls._valueAVD

    def getValueTPR(cls):
        return cls._valueTPR

    @classmethod
    @interfaceMethod
    def compareSegmentations(cls, goldStandardROI, aROIToCompare, filename):
        """
        Compares the segementation between ground truth (gold standard) ROI and test ROI
        Calculating various statistical measures
        Current values calculated are DICE, Volumetric Similarity (VS), Rand Index (RI),
        and Cohen Kappa Coefficient (KAPA)

        :param goldStandardROI: gold standard ROI
        :type goldStandardROI: ORSModel.ors.ROI
        :param aROIToCompare: ROI to compare with the gold standard
        :type aROIToCompare: ORSModel.ors.ROI
        :param filename: the file to save the results into
        :type filename: file saving
        """

        if goldStandardROI is None:
            return

        if aROIToCompare is None:
            return

        if not goldStandardROI.getHasSameShape(aROIToCompare):
            return

        #print(' getTitle of Gold standard = ', goldStandardROI.getTitle())

        # True Positive
        aROITP = aROIToCompare.getIntersectionWithROI(goldStandardROI, None)
        voxelCountTP = aROITP.getVoxelCount(0)
        valueTP = voxelCountTP

        # False Positive
        goldStandardInverse = goldStandardROI.getReversed(None)
        aROIFP = aROIToCompare.getIntersectionWithROI(goldStandardInverse, None)
        voxelCountFP = aROIFP.getVoxelCount(0)
        valueFP = voxelCountFP

        # False Negative
        aROIToCompareInverse = aROIToCompare.getReversed(None)
        aROIFN = aROIToCompareInverse.getIntersectionWithROI(goldStandardROI, None)
        voxelCountFN = aROIFN.getVoxelCount(0)
        valueFN = voxelCountFN

        # True Negative
        aROITN = aROIToCompareInverse.getIntersectionWithROI(goldStandardInverse, None)
        voxelCountTN = aROITN.getVoxelCount(0)
        valueTN = voxelCountTN

        # Calculate the various comparison statistics
        valueDSC = 2 * valueTP / (2 * valueTP + valueFP + valueFN)
        # print('Dice value = ', valueDSC)

        valueVS = 1 - (abs(valueFN-valueFP) / (2*valueTP + valueFP + valueFN))
        # print('VS value = ', valueVS)

        valueA = 0.5*(valueTP*(valueTP-1) + valueFP*(valueFP-1) + valueTN*(valueTN-1) + valueFN*(valueFN-1))
        valueB = 0.5*((valueTP+valueFN)**2 + (valueTN+valueFP)**2 - (valueTP**2 + valueTN**2 + valueFP**2 + valueFN**2))
        valueC = 0.5*((valueTP+valueFP)**2 + (valueTN+valueFN)**2 - (valueTP**2 + valueTN**2 + valueFP**2 + valueFN**2))
        valueN = goldStandardROI.getTotalVoxelCount() + goldStandardInverse.getTotalVoxelCount()
        # print(' valueN = ', valueN)
        valueD = valueN*(valueN-1)/2 - (valueA+valueB+valueC)
        #valueRI = (valueA + valueB) / (valueA + valueB + valueC + valueD)
        valueRI = (valueA + valueD) / (valueA + valueB + valueC + valueD)
        # print('RI value = ', valueRI)

        valueFa = valueTN + valueTP
        valueFc = ((valueTN+valueFN)*(valueTN+valueFP) + (valueFP+valueTP)*(valueFN+valueTP)) / valueN
        valueKAP = (valueFa - valueFc) / (valueN - valueFc)
        # print('KAP value = ', valueKAP)

        # Calculate the Huasdorff distance metric
        #    get the ndarray of the two ROI's and make sure they are 2D arrays for use in
        #    the Huasdorff distance calculation.
        goldStandardSC = ROIHelper.createFullVolumeROIWithStructuredGrid(goldStandardROI)
        goldStandardCH = Channel()
        StructuredGrid.getAsChannel(goldStandardSC, goldStandardCH, IProgress=None)
        goldStandardNP = goldStandardCH.getNDArray()

        aToCompareSC = ROIHelper.createFullVolumeROIWithStructuredGrid(aROIToCompare)
        aToCompareCH = Channel()
        StructuredGrid.getAsChannel(aToCompareSC, aToCompareCH, IProgress=None)
        aToCompareNP = aToCompareCH.getNDArray()

        valueHD1 = directed_hausdorff(goldStandardNP[0, :, :], aToCompareNP[0, :, :])
        print('Huasdorff distance gold-comp1: ', valueHD1[0])
        print('Huasdorff distance gold-comp1 index of point goldstand: ', valueHD1[1])
        print('Huasdorff distance gold-comp1 index of point toCompare: ', valueHD1[2])
        valueHD2 = directed_hausdorff(aToCompareNP[0, :, :], goldStandardNP[0, :, :])
        print('Huasdorff distance gold-comp2: ', valueHD2[0])
        print('Huasdorff distance gold-comp2 index of point toCompare: ', valueHD2[1])
        print('Huasdorff distance gold-comp2 index of point goldstand: ', valueHD2[2])
        valueAVD = (valueHD1[0] + valueHD2[0]) / 2.0

        # Calculate the True Positive Rate
        valueTPR = valueTP / (valueTP + valueFN)
        print('True Positive Rate: ', valueTPR)

        # Deleting temporary objects
        aROITP.deleteObject()
        goldStandardInverse.deleteObject()
        aROIFP.deleteObject()
        aROIFN.deleteObject()
        aROITN.deleteObject()
        aROIToCompareInverse.deleteObject()
        goldStandardSC.deleteObject()
        goldStandardCH.deleteObject()
        aToCompareSC.deleteObject()
        aToCompareCH.deleteObject()

        # Pass Results to Mainform for GUI Update
        cls._valueTP = valueTP
        cls._valueFP = valueFP
        cls._valueTN = valueTN
        cls._valueFN = valueFN
        cls._valueDSC = valueDSC
        cls._valueVS = valueVS
        cls._valueRI = valueRI
        cls._valueKAP = valueKAP
        cls._valueAVD = valueAVD
        cls._valueTPR = valueTPR

        # Writing values in CSV file
        delimiter = ','

        # Opening the file
        try:
            # fio = open(filename, "w", encoding="utf-16")
            fio = open(filename, "w")
        except Exception as exc:
            # Need to add code letting user know could not open output file...
            return

        def outputField(field, addDelimiter=True):
            fio.write(field)
            if addDelimiter:
                fio.write(delimiter)

        def outputEOL():
            fio.write('\n')

        # Column Headers
        columnNames = ['GT ROI Name', 'Compare ROI Name', 'TP', 'FP', 'TN', 'FN', 'DICE', 'VS', 'RI',
                       'KAP', 'AVD', 'TPR']

        # print(' About to write results to output file...')
        for field in columnNames[:-1]:
            outputField(field, True)

        outputField(columnNames[-1], False)
        outputEOL()

        # Values
        outputField(goldStandardROI.getTitle(), True)
        outputField(aROIToCompare.getTitle(), True)
        outputField(str(valueTP), True)
        outputField(str(valueFP), True)
        outputField(str(valueTN), True)
        outputField(str(valueFN), True)
        outputField(str(valueDSC), True)
        outputField(str(valueVS), True)
        outputField(str(valueRI), True)
        outputField(str(valueKAP), True)
        outputField(str(valueAVD), True)
        outputField(str(valueTPR), False)
        outputEOL()

        # Closing the file
        fio.close()
