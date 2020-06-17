"""
This computes the cortical and trabecular properties in the quadrent regions of an ROI. Initially developed for the femoral neck region of the proximal femur. 

:author: Daniella Patton; Robert Goulet
:contact: pattondm@umich.edu; rgoulet@med.umich.edu
:email: pattondm@umich.edu; rgoulet@med.umich.edu
:organization: Orthopeadic Research Labs, University of Michigan
:address: BSRB, 109 Zina Pitcher Place, Ann Arbor, MI 48109
:copyright: 2019
:date: Mar 07 2019 09:43
:dragonflyVersion: 4.0.0.569
:UUID: 6be3f97a40e711e9ae07005056c00008
"""

__version__ = '1.0.0'

from OrsLibraries.workingcontext import WorkingContext
from ORSServiceClass.OrsPlugin.orsPlugin import OrsPlugin
# from ORSServiceClass.decorators.decorators import run_in_background_waiting_until_finished
from ORSServiceClass.decorators.infrastructure import interfaceMethod, menuItem
from ORSServiceClass.actionAndMenu.menu import Menu
from ORSServiceClass.OrsPlugin.uidescriptor import UIDescriptor
#from ORSModel.ors import StructuredGrid, ROI
from ORSModel.ors import StructuredGrid, ROI, PerimeterComputation
from ORSModel import orsColor, ROI, Channel, Progress, Plane, Vector3, orsVect
from .mainform import MainForm
from OrsPythonPlugins.OrsVolumeROITools.OrsVolumeROITools import OrsVolumeROITools
from OrsHelpers.roihelper import ROIHelper
import numpy as np
from numpy import zeros
import pandas as pd

class BoneQuadrentAnalysis_6be3f97a40e711e9ae07005056c00008(OrsPlugin):

    # Plugin definition
    multiple = True
    closable = True
    savable = False
    keepAlive = False

    # UIs
    UIDescriptors = [UIDescriptor(name='MainForm',
                                  title='Bone Quadrent Analysis',
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
        instance = BoneQuadrentAnalysis_6be3f97a40e711e9ae07005056c00008()
        if instance is not None:
            instance.openWidget('MainForm')

    @classmethod
    @menuItem('ORL')
    def menuItemStartPlugin(cls):
        aMenuItem = Menu(title='Bone Quadrent Analysis',
                         id_='BoneQuadrentAnalysis_6be3f97a40e711e9ae07005056c00008_1',
                         section='',
                         action='BoneQuadrentAnalysis_6be3f97a40e711e9ae07005056c00008.openGUI()')
        return aMenuItem

    @classmethod
    @interfaceMethod
    def BoneQuadrentAnalysis(cls, boneROI, corticalROI, marrowROI, foldername, bCalcMarrow, bCalcCorticalSlice,
                             bCalc3DQuad, zslicePadding):
        """
        Calculates BV.TV and Thickness in 4 different marrow regions

        :param boneROI: Bone ROI
        :type boneROI: ORSModel.ors.ROI
        :param corticalROI: Cortical ROI
        :type corticalROI: ORSModel.ors.ROI
        :param marrowROI: Marrow ROI
        :type marrowROI: ORSModel.ors.ROI
        :param foldername: the folder to save the results into
        :type foldername: folder saving
        :param bCalcMarrow: flag to calculate Marrow properties
        :type bCalcMarrow: bool
        :param bCalcCorticalSlice: flag to calculate Cortical slice properties
        :type bCalcCorticalSlice: bool
        :param bCalc3DQuad: flag to calculate Cortical slice properties
        :type bCalc3DQuad: bool
        :param zslicePadding: the amount of padding (0-99) to add when calculating cortical thickness map
        :type zslicePadding: int
        """

        # Put your code here
        # Check to see if three ROIs exist
        if boneROI is None:
            return
        if corticalROI is None:
            return
        if marrowROI is None:
            return
        if not foldername:
            foldername = 'C:\ORSTemp'

        print(' Checked if ROIs okay by printing voxel count...')
        # Getting the total voxel count for each ROI
        print('The total voxel count of Bone: ', boneROI.getVoxelCount(0))
        print('The total voxel count of Cortical: ', corticalROI.getVoxelCount(0))
        print('The total voxel count of Marrow: ', marrowROI.getVoxelCount(0))
        print('The folder name is: ', foldername)
        print('The z-slice padding is:  ', zslicePadding)
        if bCalcMarrow:
            print('Calculating Marrow Spacing values...')
        else:
            print('NOT Calculating Marrow Spacing values...')
        if bCalcCorticalSlice:
            print('Calculating Cortical Slice Properites...')
        else:
            print('NOT Calculating Cortical Slice Properites...')
        if bCalc3DQuad:
            print('Calculating 3D Quadrent Properites...')
        else:
            print('NOT Calculating 3D Quadrent Properites...')

        # Instantiation of the progress object
        progress = Progress()
        # NOTE: Using code from the DemoProgress plugin, but only implementing part of code that gives/shows estimated
        #       time remaining for analysis as not sure how long (or percent left) it will really take.
        isProgressBarCancellable = False
        progressWindowTitle = 'Bone Analysis is Running'
        progress.startWorkingProgressWithCaption(progressWindowTitle, isProgressBarCancellable)
        # Calling a method run in another thread
        # cls._methodInAnotherThread(progress, isProgressBarCancellable,
        #                            boneROI, corticalROI, marrowROI, foldername, bCalcMarrow)

        # Closing and deletion of the progress object
        # progress.deleteObject()

        # Return
        #return

    # @run_in_background_waiting_until_finished
    # def _methodInAnotherThread(self, progress, isProgressBarCancellable,
    #                          boneROI, corticalROI, marrowROI, foldername, bCalcMarrow):
        if bCalc3DQuad:
            # Open progress dialog window. Open to just have progress bar loop back and forth as can't really estimate when
            # analysis will be finished (or percentage left).
            # progressWindowTitle = 'Evaluating Thicknesses'
            #progress.startWorkingProgressWithCaption(progressWindowTitle, isProgressBarCancellable)
            progress.setExtraText('Determining 3D halves...')

            # Get Union of the Cortical and Marrow ROI's to use to get the Center of Mass
            # or centroid in each slice
            # Get union of Cortical and Marrow ROI's to get the center of mass (centroid)
            aTotalROI = corticalROI.copy()
            aTotalROI.addROI(marrowROI)
            # aTotalROI.setTitle('Total Crossectional ROI')
            # aTotalROI.publish()

            # Check every-now-and-then to see if hit 'Cancel' button in progress dialog window...
            #   if progress is not None and progress.getIsCancelled():
                # Breaking the evaluation
            #       break

            # Need to extract a single slice (z-index) to determine the center of mass and iterate for all slices
            # We need to extract a single slice from structured gridROI(aTotalROI converted to structured grid)
            # convert ROI from single slice to structured grid
            aROISG = ROIHelper.createFullVolumeROIWithStructuredGrid(aTotalROI)
            # Find the dimensions and save the z-dimension of the Structured Grid
            zSize = aROISG.getZSize()
            print(' X Size: ', aROISG.getXSize(), ' Y Size: ', aROISG.getYSize(), ' Z Size: ', zSize)
            xSpacing = aROISG.getXSpacing()
            print('X Spacing = ', xSpacing)

            # Need to create a channel from the ROI Structured grid to define the region to highlight in the loop
            aROIC = Channel()
            StructuredGrid.getAsChannel(aROISG, aROIC, IProgress=None) # the min max value is 1,1
            #StructuredGrid.getAsChannel(aROISG, aROIC, IProgress=progress)  # the min max value is 1,1
            # Find the min and max value of the channel to know what to highlight in are
            # double checking that the shape  of the new channel is the same as the structured grid
            #debug print('Printing the size of channel is: x size, ', aROIC.getXSize(), 'y size: ', aROIC.getYSize(), 'z size: ', aROIC.getZSize())
            # aROIC.setTitle('A ROI structured grid as channel')
            # aROIC.publish()
            #ROI Superior 1
            roiSuperior1 = ROI()
            roiSuperior1.setTitle('roiSuperior1')
            roiSuperior1.copyShapeFromStructuredGrid(aTotalROI)
            roiSuperior1.setInitialColor(orsColor(1, 0, 0, 1))
            #ROI Inferior 1
            roiInferior1 = ROI()
            roiInferior1.setTitle('roiInferior1')
            roiInferior1.copyShapeFromStructuredGrid(aTotalROI)
            roiInferior1.setInitialColor(orsColor(1, 0, 0, 1))
            # ROI Superior 2
            roiSuperior2 = ROI()
            roiSuperior2.setTitle('roiSuperior2')
            roiSuperior2.copyShapeFromStructuredGrid(aTotalROI)
            roiSuperior2.setInitialColor(orsColor(1, 0, 0, 1))
            # ROI Inferior 2
            roiInferior2 = ROI()
            roiInferior2.setTitle('roiInferior2')
            roiInferior2.copyShapeFromStructuredGrid(aTotalROI)
            roiInferior2.setInitialColor(orsColor(1, 0, 0, 1))

            # Two loops need to be run in order to segment the volume of interest into four regions
            if zSize == 1:
                izs = 1
                ize = 2
            else:
                izs = 1
                print('round(zSize / 2) is equal to', round(zSize / 2))
                ize = round(zSize / 2) + 1

            print('Starting iz loop of lower half for izs to ize: ', izs, ize)
            for iz in range(izs, ize):
                #debug print('Working on lower half iz slice ', iz)
                singleSliceSG = StructuredGrid.getSliceAtIndex(aROISG, iz, aROISG, IProgress=None)
                #singleSliceSG = StructuredGrid.getSliceAtIndex(aROISG, iz, aROISG, IProgress=progress)
                singleSliceROI = ROIHelper.createROIFromStructuredGrid(singleSliceSG, 'Single Slice ROI', orsColor(1, 0, 0, 1))
                originSingleSlice = singleSliceSG.getOrigin()
                #debug print(' Origin for Single Slice SG: ', originSingleSlice)
                vCenterMass = singleSliceROI.getCenterOfMass(0)
                #debug print(' Center of mass for Total ROI: ', vCenterMass)
                voxCenterMass = StructuredGrid.getWorldToVoxelCoordinates(singleSliceSG, vCenterMass)
                #debug print(' Voxel Center of mass for Total ROI: ', voxCenterMass)

                xSize2 = singleSliceROI.getXSize()
                ySize2 = singleSliceROI.getYSize()
                zSize2 = singleSliceROI.getZSize()
                #debug print(' X Size: ', xSize2, ' Y Size: ', ySize2, ' Z Size: ', zSize2)
                #debug print('Single Slice ROI has been created')
                xCentroid = int((voxCenterMass[0] - originSingleSlice[0]) / xSpacing)
                #debug print('The calculated x centroid ', xCentroid)
                aROIC.getAsROIWithinRangeInArea(1, 1, 0, 0, (iz-1), (xCentroid - 1), (aROIC.getYSize()-1), (iz-1), None,
                                                roiInferior1)
                aROIC.getAsROIWithinRangeInArea(1, 1, xCentroid, 0, (iz - 1), (aROIC.getXSize() - 1),
                                                (aROIC.getYSize() - 1), (iz - 1), None, roiSuperior1)
                # delete temp Structure grid and ROI created for current slice.
                singleSliceSG.deleteObject()
                singleSliceROI.deleteObject()

            # if the z size is equal 1 one, repeat analysis on the same section and output results
            if zSize == 1:
                izs = 1
                ize = 2
            else:
                izs = round(zSize / 2) + 1
                ize = zSize + 1

            print(' Working on upper half slices, izs to ize: ', izs, ize)
            for iz in range(izs, ize):
                #debug print('Working on upper half iz slice ', iz)
                singleSliceSG = StructuredGrid.getSliceAtIndex(aROISG, iz, aROISG, IProgress=None)
                #singleSliceSG = StructuredGrid.getSliceAtIndex(aROISG, iz, aROISG, IProgress=progress)
                singleSliceROI = ROIHelper.createROIFromStructuredGrid(singleSliceSG, 'Single Slice ROI', orsColor(1, 0, 0, 1))
                originSingleSlice = singleSliceSG.getOrigin()
                #debug print(' Origin for Single Slice SG: ', originSingleSlice)
                vCenterMass = singleSliceROI.getCenterOfMass(0)
                #debug print(' Center of mass for Total ROI: ', vCenterMass)
                voxCenterMass = StructuredGrid.getWorldToVoxelCoordinates(singleSliceSG, vCenterMass)
                #debug print(' Voxel Center of mass for Total ROI: ', voxCenterMass)

                xSize2 = singleSliceROI.getXSize()
                ySize2 = singleSliceROI.getYSize()
                zSize2 = singleSliceROI.getZSize()
                #debug print(' X Size: ', xSize2, ' Y Size: ', ySize2, ' Z Size: ', zSize2)
                #debug print('Single Slice ROI has been created')
                xCentroid = int((voxCenterMass[0] - originSingleSlice[0]) / xSpacing)
                #debug print('The calculated x centroid ', xCentroid)
                aROIC.getAsROIWithinRangeInArea(1, 1, 0, 0, (iz-1), (xCentroid - 1), (aROIC.getYSize()-1), (iz-1), None,
                                                roiInferior2)
                aROIC.getAsROIWithinRangeInArea(1, 1, xCentroid, 0, (iz - 1), (aROIC.getXSize() - 1),
                                                (aROIC.getYSize() - 1), (iz - 1), None, roiSuperior2)
                singleSliceSG.deleteObject()
                singleSliceROI.deleteObject()

            print('Finished analyzing slices')
            # Delete unnecessary variables
            #debug print('   deleting unnecessary objects...')
            del zSize, ize, izs, originSingleSlice, vCenterMass, voxCenterMass

            # Can Potentially Delete: aROISG, aROIC zSize izs and ize singleSliceSG, singleSliceROI, originSingleSlice
            # vCenterMass, voxCenterMass

            print('Stating region analysis to get various properties')
            # The data-set has now been Split into Superior and Inferior ROIs in four regions
            # This is where we need to quantify to average thickness each region
            # Cortical thickness and BV/TV measures
            # From the Cortical ROI get the average cortical thickness of the entire volume
            currentTime = 0
            print(' ')
            print(' Finding Cortical Volume Thickness')
            progress.setExtraText('Finding Cortical Volume Thickness...')
            # Need to create a new volume thickness channel with the z-padding added
            # the padding is a copy of the first and last z-slice in the volume thickness channel z-times
            # set it sizes, since we use the default voxel size, the channel is for now 100 meter cube
            if zslicePadding == 0:
                aCortVolumeThicknessChannel = OrsVolumeROITools.createVolumeThicknessFromROI(corticalROI,
                                                                                             currentTime=currentTime,
                                                                                             IProgress=None)
            else:
                paddedCortROI = corticalROI.copy()
                # paddedCortROISG = ROIHelper.createFullVolumeROIWithStructuredGrid(paddedCortROI)
                orig_zsize = corticalROI.getZSize()
                padded_zsize = orig_zsize + (2*zslicePadding)
                paddedCortROI.setZSize(padded_zsize)
                box_paddedCortROISG = paddedCortROI.getBox()
                paddedCortROISG_direction2 = box_paddedCortROISG.getDirection2()
                paddedCortROISG_spacingdirection2 = box_paddedCortROISG.getDirection2Spacing()
                paddedCortROISG_origin = box_paddedCortROISG.getOrigin()
                paddedCortROISG_neworigin = paddedCortROISG_origin - (zslicePadding * paddedCortROISG_spacingdirection2
                                            * paddedCortROISG_direction2)
                box_paddedCortROISG.setOrigin(paddedCortROISG_neworigin)
                paddedCortROI.setBox(box_paddedCortROISG)
                paddedCortROI.clearROI()
                # paddedCortROISG.clearROI()
                timeStep = 0
                # Copy the common region data
                paddedCortROI.addROI(corticalROI)

                # Padding at the lower z
                tempROILowerZ = corticalROI.getSubset(0, 0, 0, timeStep, paddedCortROI.getXSize()-1,
                                                          paddedCortROI.getYSize()-1, 0, timeStep, None, None)

                for zi in range(zslicePadding):
                    originToSet = paddedCortROI.getVoxelToWorldCoordinates(orsVect(0, 0, zi))
                    tempROILowerZ.setOrigin(originToSet)
                    paddedCortROI.addROI(tempROILowerZ)
                tempROILowerZ.deleteObject()

                # Padding at the higher z
                tempROIHigherZ = corticalROI.getSubset(0, 0, orig_zsize-1, timeStep, paddedCortROI.getXSize() - 1,
                                                      paddedCortROI.getYSize() - 1, orig_zsize-1, timeStep, None, None)
                for zi in range(zslicePadding):
                    originToSet = paddedCortROI.getVoxelToWorldCoordinates(orsVect(0, 0, padded_zsize - 1 - zi))
                    tempROIHigherZ.setOrigin(originToSet)
                    paddedCortROI.addROI(tempROIHigherZ)
                tempROIHigherZ.deleteObject()

                paddedCortROI.setTitle(corticalROI.getTitle() + 'Padded')
                # paddedCortROI.publish()

                aCortVolumeThicknessChannel = OrsVolumeROITools.createVolumeThicknessFromROI(paddedCortROI,
                                                                                             currentTime=currentTime,
                                                                                             IProgress=None)
                paddedCortROI.deleteObject()



            #IProgress = None)
            print(' ')
            print('   found Cortical Volume Thickness...')
            # aCortVolumeThicknessChannel.setTitle('Cort Volume thickness ROI')
            # aCortVolumeThicknessChannel.publish()
            # Now that the thickness map created for the cortical volume we need to ge average cortical thickness for
            # each region
            # Cortical Results will be calculated first

            # Total Cortical Region
            # Calculating the min, mean, max, and SD cortical thickness in addition to BV/TV in that region
            # Cortical: Total BV/TV
            print('   Calculating Cortical BV/TV')
            cortBoneROI = corticalROI.getIntersectionWithROI(boneROI, None)
            cortBVTV = ROI.getTotalVoxelCount(cortBoneROI) / ROI.getTotalVoxelCount(corticalROI)  # exported value
            # Cortical: Total thickness min, mean, max, and SD
            minCortTh = ROI.getMinSourceDataValue(corticalROI, currentTime, aCortVolumeThicknessChannel)  # exported value
            maxCortTh = ROI.getMaxSourceDataValue(corticalROI, currentTime, aCortVolumeThicknessChannel)  # exported value
            meanCortTh = ROI.getMeanSourceDataValue(corticalROI, currentTime, aCortVolumeThicknessChannel)  # exported value
            sdCortTh = ROI.getStandardDeviationSourceDataValue(corticalROI, currentTime, aCortVolumeThicknessChannel)  # exported value
            # totVoxCortTh = ROI.getTotalVoxelCount(corticalROI)  # exported value
            print(' ')
            print('   found overall Cortical BV_TV...')

            # Regional Cortical analysis (4 different regions)
            # Cortical: Superior 1
            # Cortical: Superior 1 BV/TV
            aCortSup1ROI = corticalROI.getIntersectionWithROI(roiSuperior1, None)
            cortSup1BoneROI = aCortSup1ROI.getIntersectionWithROI(boneROI, None)
            cortSup1BVTV = ROI.getTotalVoxelCount(cortSup1BoneROI) / ROI.getTotalVoxelCount(aCortSup1ROI)  # exported value
            #debug print('CortSup1 BV/TV: ', cortSup1BVTV)
            # Cortical: Superior 1 thickness min, mean, max, and SD
            minCortSup1 = ROI.getMinSourceDataValue(aCortSup1ROI, currentTime, aCortVolumeThicknessChannel)
            maxCortSup1 = ROI.getMaxSourceDataValue(aCortSup1ROI, currentTime, aCortVolumeThicknessChannel)
            #debug print('maxCortSup1: ', maxCortSup1)
            meanCortSup1 = ROI.getMeanSourceDataValue(aCortSup1ROI, currentTime, aCortVolumeThicknessChannel)
            #debug print('meanCortSup1: ', meanCortSup1)
            sdCortSup1 = ROI.getStandardDeviationSourceDataValue(aCortSup1ROI, currentTime, aCortVolumeThicknessChannel)
            #debug print('sdCortSup1: ', sdCortSup1)
            #totVoxCortSup1 = ROI.getTotalVoxelCount(aCortSup1ROI)
            #print('totVoxCortSup1: ', totVoxCortSup1)
            print(' ')
            print('   finished cortical superior 1...')

            # Cortical: Superior 2 BV/TV
            aCortSup2ROI = corticalROI.getIntersectionWithROI(roiSuperior2, None)
            cortSup2BoneROI = aCortSup2ROI.getIntersectionWithROI(boneROI, None)
            cortSup2BVTV = ROI.getTotalVoxelCount(cortSup2BoneROI) / ROI.getTotalVoxelCount(aCortSup2ROI)  # exported value
            # Cortical: Superior 2 thickness min, mean, max, and SD
            minCortSup2 = ROI.getMinSourceDataValue(aCortSup2ROI, currentTime, aCortVolumeThicknessChannel)
            maxCortSup2 = ROI.getMaxSourceDataValue(aCortSup2ROI, currentTime, aCortVolumeThicknessChannel)
            meanCortSup2 = ROI.getMeanSourceDataValue(aCortSup2ROI, currentTime, aCortVolumeThicknessChannel)
            sdCortSup2 = ROI.getStandardDeviationSourceDataValue(aCortSup2ROI, currentTime, aCortVolumeThicknessChannel)
            # totVoxCortSup2 = ROI.getTotalVoxelCount(aCortSup2ROI)
            print(' ')
            print('   finished cortical superior 2...')

            # Cortical: Inferior 1 BV/TV
            aCortInf1ROI = corticalROI.getIntersectionWithROI(roiInferior1, None)
            CortInf1BoneROI = aCortInf1ROI.getIntersectionWithROI(boneROI, None)
            CortInf1BVTV = ROI.getTotalVoxelCount(CortInf1BoneROI) / ROI.getTotalVoxelCount(aCortInf1ROI)  # exported value
            # Cortical: Inferior 1 thickness min, mean, max, and SD
            minCortInf1 = ROI.getMinSourceDataValue(aCortInf1ROI, currentTime, aCortVolumeThicknessChannel)
            maxCortInf1 = ROI.getMaxSourceDataValue(aCortInf1ROI, currentTime, aCortVolumeThicknessChannel)
            meanCortInf1 = ROI.getMeanSourceDataValue(aCortInf1ROI, currentTime, aCortVolumeThicknessChannel)
            sdCortInf1 = ROI.getStandardDeviationSourceDataValue(aCortInf1ROI, currentTime, aCortVolumeThicknessChannel)
            # totVoxCortInf1 = ROI.getTotalVoxelCount(aCortInf1ROI)
            print(' ')
            print('   finished cortical inferior 1...')

            # Cortical: Inferior 2 BV/TV
            aCortInf2ROI = corticalROI.getIntersectionWithROI(roiInferior2, None)
            CortInf2BoneROI = aCortInf2ROI.getIntersectionWithROI(boneROI, None)
            CortInf2BVTV = ROI.getTotalVoxelCount(CortInf2BoneROI) / ROI.getTotalVoxelCount(aCortInf2ROI)  # exported value
            # Cortical: Inferior 2 thickness min, mean, max, and SD
            minCortInf2 = ROI.getMinSourceDataValue(aCortInf2ROI, currentTime, aCortVolumeThicknessChannel)
            maxCortInf2 = ROI.getMaxSourceDataValue(aCortInf2ROI, currentTime, aCortVolumeThicknessChannel)
            meanCortInf2 = ROI.getMeanSourceDataValue(aCortInf2ROI, currentTime, aCortVolumeThicknessChannel)
            sdCortInf2 = ROI.getStandardDeviationSourceDataValue(aCortInf2ROI, currentTime, aCortVolumeThicknessChannel)
            # totVoxCortInf2 = ROI.getTotalVoxelCount(aCortInf2ROI)
            print(' ')
            print('   finished cortical inferior 2...')

            # aCortVolumeThicknessChannelTakes up a lof of memory, need to delete
            # aCortVolumeThicknessChannel.deleteObject()
            cortBoneROI.deleteObject()
            aCortSup1ROI.deleteObject()
            cortSup1BoneROI.deleteObject()
            aCortSup2ROI.deleteObject()
            cortSup2BoneROI.deleteObject()
            aCortInf1ROI.deleteObject()
            CortInf1BoneROI.deleteObject()
            aCortInf2ROI.deleteObject()
            CortInf2BoneROI.deleteObject()

            # Trabecular measures all and regional measures
            # Average Trabecular measures
            # From the ROI's get the trabecular bone within the marrow ROI
            # Trabecular: Total BV/TV
            aTrabBoneROI = marrowROI.getIntersectionWithROI(boneROI, None)
            # Find Volume ROI thickness of the Trabecular and Marrow space
            print(' ')
            print('Finding Trabecular Volume Thickness...')
            progress.setExtraText('Finding Trabecular Volume Thickness...')
            aTrabVolumeThicknessChannel = OrsVolumeROITools.createVolumeThicknessFromROI(aTrabBoneROI,
                                                                                         currentTime=currentTime,
                                                                                         IProgress=None)
            #IProgress = None)
            print(' ')
            print('   found Trabecular Volume Thickness...')
            # aTrabVolumeThicknessChannel.setTitle('Trab Volume thickness ROI')
            # aTrabVolumeThicknessChannel.publish()
            trabBVTV = ROI.getTotalVoxelCount(aTrabBoneROI) / ROI.getTotalVoxelCount(marrowROI)  # exported value
            # Trabecular: Total thickness min, mean, max, and SD
            minTrabTh = ROI.getMinSourceDataValue(aTrabBoneROI, currentTime, aTrabVolumeThicknessChannel)  # exported value
            maxTrabTh = ROI.getMaxSourceDataValue(aTrabBoneROI, currentTime, aTrabVolumeThicknessChannel)  # exported value
            meanTrabTh = ROI.getMeanSourceDataValue(aTrabBoneROI, currentTime, aTrabVolumeThicknessChannel)  # exported value
            sdTrabTh = ROI.getStandardDeviationSourceDataValue(aTrabBoneROI, currentTime,
                                                               aTrabVolumeThicknessChannel)  # exported value
            print(' ')
            print('   found overall Trabecular BV_TV...')

            # Trabecular: Superior 1 BV/TV
            aTrabSup1ROI = marrowROI.getIntersectionWithROI(roiSuperior1, None)
            trabSup1BoneROI = aTrabSup1ROI.getIntersectionWithROI(boneROI, None)
            trabSup1BVTV = ROI.getTotalVoxelCount(trabSup1BoneROI) / ROI.getTotalVoxelCount(aTrabSup1ROI)  # exported value
            # Trabecular: Superior 1 thickness min, mean, max, and SD
            minTrabSup1 = ROI.getMinSourceDataValue(trabSup1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            maxTrabSup1 = ROI.getMaxSourceDataValue(trabSup1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            meanTrabSup1 = ROI.getMeanSourceDataValue(trabSup1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            sdTrabSup1 = ROI.getStandardDeviationSourceDataValue(trabSup1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            print(' ')
            print('   finished trab superior 1...')

            # Trabecular: Superior 2 BV/TV
            aTrabSup2ROI = marrowROI.getIntersectionWithROI(roiSuperior2, None)
            trabSup2BoneROI = aTrabSup2ROI.getIntersectionWithROI(boneROI, None)
            trabSup2BVTV = ROI.getTotalVoxelCount(trabSup2BoneROI) / ROI.getTotalVoxelCount(aTrabSup2ROI)  # exported value
            # Trabecular: Superior 1 thickness min, mean, max, and SD
            minTrabSup2 = ROI.getMinSourceDataValue(trabSup2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            maxTrabSup2 = ROI.getMaxSourceDataValue(trabSup2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            meanTrabSup2 = ROI.getMeanSourceDataValue(trabSup2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            sdTrabSup2 = ROI.getStandardDeviationSourceDataValue(trabSup2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            print(' ')
            print('   finished trab superior 2...')

            # Trabecular: Inferior 1 BV/TV
            aTrabInf1ROI = marrowROI.getIntersectionWithROI(roiInferior1, None)
            trabInf1BoneROI = aTrabInf1ROI.getIntersectionWithROI(boneROI, None)
            trabInf1BVTV = ROI.getTotalVoxelCount(trabInf1BoneROI) / ROI.getTotalVoxelCount(aTrabInf1ROI)  # exported value
            # Trabecular: Inferior 1 thickness min, mean, max, and SD
            minTrabInf1 = ROI.getMinSourceDataValue(trabInf1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            maxTrabInf1 = ROI.getMaxSourceDataValue(trabInf1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            meanTrabInf1 = ROI.getMeanSourceDataValue(trabInf1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            sdTrabInf1 = ROI.getStandardDeviationSourceDataValue(trabInf1BoneROI, currentTime, aTrabVolumeThicknessChannel)
            print(' ')
            print('   finished trab inferior 1...')

            # Trabecular: Inferior 2 BV/TV
            aTrabInf2ROI = marrowROI.getIntersectionWithROI(roiInferior2, None)
            trabInf2BoneROI = aTrabInf2ROI.getIntersectionWithROI(boneROI, None)
            trabInf2BVTV = ROI.getTotalVoxelCount(trabInf2BoneROI) / ROI.getTotalVoxelCount(aTrabInf2ROI)  # exported value
            # Trabecular: Inferior 2 thickness min, mean, max, and SD
            minTrabInf2 = ROI.getMinSourceDataValue(trabInf2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            maxTrabInf2 = ROI.getMaxSourceDataValue(trabInf2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            meanTrabInf2 = ROI.getMeanSourceDataValue(trabInf2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            sdTrabInf2 = ROI.getStandardDeviationSourceDataValue(trabInf2BoneROI, currentTime, aTrabVolumeThicknessChannel)
            print(' ')
            print('   finished trab inferior 2...')

            # aCortVolumeThicknessChannelTakes up a lof of memory, need to delete; as well as the other temp Objects
            aTrabBoneROI.deleteObject()
            aTrabVolumeThicknessChannel.deleteObject()
            aTrabSup1ROI.deleteObject()
            trabSup1BoneROI.deleteObject()
            aTrabSup2ROI.deleteObject()
            trabSup2BoneROI.deleteObject()
            aTrabInf1ROI.deleteObject()
            trabInf1BoneROI.deleteObject()
            aTrabInf2ROI.deleteObject()
            trabInf2BoneROI.deleteObject()

            # Marrow Spacing
            if bCalcMarrow:
                # From the Marrow ROI get the average trabecular spacing
                roiMarrowSpacing = marrowROI.copy()
                roiMarrowSpacing.removeROI(aTrabBoneROI)
                print(' ')
                print('Finding Marrow Volume Thickness')
                progress.setExtraText('Finding Marrow Volume Thickness...')
                aMarrowSpacingVolumeThicknessChannel = OrsVolumeROITools.createVolumeThicknessFromROI(roiMarrowSpacing,
                                                                                                  currentTime=currentTime,
                                                                                                  IProgress=progress)
                #IProgress = None)
                print(' ')
                print('   found Marrow Volume Thickness...')
                # aMarrowSpacingVolumeThicknessChannel.setTitle("Marrow Volume thickness ROI")
                # aMarrowSpacingVolumeThicknessChannel.publish()
                # Marrow Spacing: Total seperation min, mean, max, and SD
                minMarrow = ROI.getMinSourceDataValue(roiMarrowSpacing, currentTime, aMarrowSpacingVolumeThicknessChannel)
                maxMarrow = ROI.getMaxSourceDataValue(roiMarrowSpacing, currentTime, aMarrowSpacingVolumeThicknessChannel)
                meanMarrow = ROI.getMeanSourceDataValue(roiMarrowSpacing, currentTime, aMarrowSpacingVolumeThicknessChannel)
                sdMarrow = ROI.getStandardDeviationSourceDataValue(roiMarrowSpacing, currentTime, aMarrowSpacingVolumeThicknessChannel)
                print(' ')
                print('   found overall Marrow thickness...')

                # Marrow: Superior 1 separation min, mean, max, and SD
                aMarrowSup1ROI = roiMarrowSpacing.getIntersectionWithROI(roiSuperior1, None)
                minMarrowSup1 = ROI.getMinSourceDataValue(aMarrowSup1ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                maxMarrowSup1 = ROI.getMaxSourceDataValue(aMarrowSup1ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                meanMarrowSup1 = ROI.getMeanSourceDataValue(aMarrowSup1ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                sdMarrowsup1 = ROI.getStandardDeviationSourceDataValue(aMarrowSup1ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                print(' ')
                print('   finished marrow superior 1...')

                # Marrow: Superior 2 separation min, mean, max, and SD
                aMarrowSup2ROI = roiMarrowSpacing.getIntersectionWithROI(roiSuperior2, None)
                minMarrowSup2 = ROI.getMinSourceDataValue(aMarrowSup2ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                maxMarrowSup2 = ROI.getMaxSourceDataValue(aMarrowSup2ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                meanMarrowSup2 = ROI.getMeanSourceDataValue(aMarrowSup2ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                sdMarrowsup2 = ROI.getStandardDeviationSourceDataValue(aMarrowSup2ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                print(' ')
                print('   finished marrow superior 2...')

                # Marrow: Inferior 1 separation min, mean, max, and SD
                aMarrowInf1ROI = roiMarrowSpacing.getIntersectionWithROI(roiInferior1, None)
                minMarrowInf1 = ROI.getMinSourceDataValue(aMarrowInf1ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                maxMarrowInf1 = ROI.getMaxSourceDataValue(aMarrowInf1ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                meanMarrowInf1 = ROI.getMeanSourceDataValue(aMarrowInf1ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                sdMarrowInf1 = ROI.getStandardDeviationSourceDataValue(aMarrowInf1ROI, currentTime,
                                                                   aMarrowSpacingVolumeThicknessChannel)
                print(' ')
                print('   finished marrow inferior 1...')

                # Marrow: Superior 2 separation min, mean, max, and SD
                aMarrowInf2ROI = roiMarrowSpacing.getIntersectionWithROI(roiInferior2, None)
                minMarrowInf2 = ROI.getMinSourceDataValue(aMarrowInf2ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                maxMarrowInf2 = ROI.getMaxSourceDataValue(aMarrowInf2ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                meanMarrowInf2 = ROI.getMeanSourceDataValue(aMarrowInf2ROI, currentTime, aMarrowSpacingVolumeThicknessChannel)
                sdMarrowInf2 = ROI.getStandardDeviationSourceDataValue(aMarrowInf2ROI, currentTime,
                                                                   aMarrowSpacingVolumeThicknessChannel)
                print(' ')
                print('   finished marrow inferior 2...')

                # delete various temp ROI's created that are no longer needed
                # aMarrowVolumeThicknessChannelTakes up a lof of memory, need to delete
                roiMarrowSpacing.deleteObject()
                aMarrowSpacingVolumeThicknessChannel.deleteObject()
                aMarrowSup1ROI.deleteObject()
                aMarrowSup2ROI.deleteObject()
                aMarrowInf1ROI.deleteObject()
                aMarrowInf2ROI.deleteObject()
            else:
                # Set marrow properties would calculate to 0.0 so can print those columns out to allow easier merging
                # of results where may have calculated the marrow spacing properties.
                print(' ')
                print('Setting Marrow Spacing properties to 0.0')
                minMarrow = 0.0
                maxMarrow = 0.0
                meanMarrow = 0.0
                sdMarrow = 0.0
                # print(' ')
                # print('   found overall Marrow thickness...')

                # Marrow: Superior 1 separation min, mean, max, and SD
                minMarrowSup1 = 0.0
                maxMarrowSup1 = 0.0
                meanMarrowSup1 = 0.0
                sdMarrowsup1 = 0.0
                # print(' ')
                # print('   finished marrow superior 1...')

                # Marrow: Superior 2 separation min, mean, max, and SD
                minMarrowSup2 = 0.0
                maxMarrowSup2 = 0.0
                meanMarrowSup2 = 0.0
                sdMarrowsup2 = 0.0
                # print(' ')
                # print('   finished marrow superior 2...')

                # Marrow: Inferior 1 separation min, mean, max, and SD
                minMarrowInf1 = 0.0
                maxMarrowInf1 = 0.0
                meanMarrowInf1 = 0.0
                sdMarrowInf1 = 0.0
                # print(' ')
                # print('   finished marrow inferior 1...')

                # Marrow: Superior 2 separation min, mean, max, and SD
                minMarrowInf2 = 0.0
                maxMarrowInf2 = 0.0
                meanMarrowInf2 = 0.0
                sdMarrowInf2 = 0.0
                # print(' ')
                # print('   finished marrow inferior 2...')

            # Delete ROI's created for the Inferior and Superior sections of each half
            roiInferior1.deleteObject()
            roiSuperior2.deleteObject()
            roiInferior2.deleteObject()
            roiSuperior1.deleteObject()

            # Save results to CSV file
            # csv filename with patch is create from the folder selcted and the base name of the bone ROI selected
            outputfilename = str(foldername) + '/' + str(ROI.getTitle(boneROI)) + '.csv'
            print('The title of BoneROI is: ', outputfilename)
            progress.setExtraText('Writing out results...')

            # If not changed the output results will be displayed
            # convert to mm
            factor = 1000
            # csv delimiter
            delimiter = ','
            # Opening the file
            try:
                fio = open(outputfilename, "w")
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
            columnNames = ['Bone_ROI_Name', 'Cortical_ROI_Name', 'Marrow_ROI_Name', 'Units',

                           'Cortical_Total_BVTV', 'Cortical_Total_mean_thick',
                           'Cortical_Total_sd_thick', 'Cortical_Total_min_thick', 'Cortical_Total_max_thick',
                           'Trabecular_Total_BVTV', 'Trabecular_Total_mean_thick', 'Trabecular_Total_sd_thick',
                           'Trabecular_Total_thick', 'Trabecular_Total_max_thick', 'Marrow_Total_mean_sep',
                           'Marrow_Total_sd_sep', 'Marrow_Total_min_sep', 'Marrow_Total_max_sep',

                           'Cortical_Sup1_BVTV', 'Cortical_Sup1_mean_thick',
                           'Cortical_Sup1_sd_thick', 'Cortical_Sup1_min_thick', 'Cortical_Sup1_max_thick',
                           'Trabecular_Sup1_BVTV', 'Trabecular_Sup1_mean_thick',
                           'Trabecular_Sup1_sd_thick', 'Trabecular_Sup1_min_thick', 'Trabecular_Sup1_max_thick',
                           'Marrow_Sup1_mean_sep', 'Marrow_Sup1_sd_sep', 'Marrow_Sup1_min_sep',
                           'Marrow_Sup1_max_sep',

                           'Cortical_Sup2_BVTV', 'Cortical_Sup2_mean_thick',
                           'Cortical_Sup2_sd_thick', 'Cortical_Sup2_min_thick', 'Cortical_Sup2_max_thick',
                           'Trabecular_Sup2_BVTV', 'Trabecular_Sup2_mean_thick',
                           'Trabecular_Sup2_sd_thick', 'Trabecular_Sup2_min_thick', 'Trabecular_Sup2_max_thick',
                           'Marrow_Sup2_mean_sep', 'Marrow_Sup2_sd_sep', 'Marrow_Sup2_min_sep',
                           'Marrow_Sup2_max_sep',

                           'Cortical_Inf1_BVTV', 'Cortical_Inf1_mean_thick',
                           'Cortical_Inf1_sd_thick', 'Cortical_Inf1_min_thick', 'Cortical_Inf1_max_thick',
                           'Trabecular_Inf1_BVTV', 'Trabecular_Inf1_mean_thick',
                           'Trabecular_Inf1_sd_thick', 'Trabecular_Inf1_min_thick', 'Trabecular_Inf1_max_thick',
                           'Marrow_Inf1_mean_sep', 'Marrow_Inf1_sd_sep', 'Marrow_Inf1_min_sep',
                           'Marrow_Inf1_max_sep',

                           'Cortical_Inf2_BVTV', 'Cortical_Inf2_mean_thick',
                           'Cortical_Inf2_sd_thick', 'Cortical_Inf2_min_thick', 'Cortical_Inf2_max_thick',
                           'Trabecular_Inf2_BVTV', 'Trabecular_Inf2_mean_thick',
                           'Trabecular_Inf2_sd_thick', 'Trabecular_Inf2_min_thick', 'Trabecular_Inf2_max_thick',
                           'Marrow_Inf2_mean_sep', 'Marrow_Inf2_sd_sep', 'Marrow_Inf2_min_sep',
                           'Marrow_Inf2_max_sep',
                           ]
            print(' About to write results to output file...')
            for field in columnNames[:-1]:
                outputField(field, True)

            outputField(columnNames[-1], False)
            outputEOL()

            # Values
            outputField(boneROI.getTitle(), True)
            outputField(corticalROI.getTitle(), True)
            outputField(marrowROI.getTitle(), True)
            outputField('mm', True)
            # Total Bone Results
            # Total Cortical
            # cortBVTV minCortTh maxCortTh meanCortTh sdCortTh totVoxCortTh
            outputField(str(cortBVTV), True)  # Cortical_Total_BVTV
            outputField(str(meanCortTh * factor), True)  # Cortical_Total_mean_thick_mm
            outputField(str(sdCortTh * factor), True)  # Cortical_Total_sd_thick_mm
            outputField(str(minCortTh * factor), True)  # Cortical_Total_min_thick_mm
            outputField(str(maxCortTh * factor), True)  # Cortical_Total_max_thick_mm
            # Total Trabeuclar
            # trabBVTV minTrabTh maxTrabTh meanTrabTh sdTrabTh
            outputField(str(trabBVTV), True)  # Trabecular_Total_BVTV
            outputField(str(meanTrabTh * factor), True)  # Trabecular_Total_mean_thick_mm
            outputField(str(sdTrabTh * factor), True)  # Trabecular_Total_sd_thick_mm
            outputField(str(minTrabTh * factor), True)  # Trabecular_Total_min_thick_mm
            outputField(str(maxTrabTh * factor), True)  # Trabecular_Total_max_thick_mm
            # Total Marrow
            #  minMarrow  maxMarrow meanMarrow sdMarrow
            outputField(str(meanMarrow * factor), True)  # Marrow_Total_mean_sep_mm
            outputField(str(sdMarrow * factor), True)  # Marrow_Total_sd_sep_mm
            outputField(str(minMarrow * factor), True)  # Marrow_Total_min_sep_mm
            outputField(str(maxMarrow * factor), True)  # Marrow_Total_max_sep_mm

            # Superior 1
            # Superior 1: Cortical
            outputField(str(cortSup1BVTV), True)  # Cortical_Sup1_BVTV
            outputField(str(meanCortSup1 * factor), True)  # Cortical_Sup1_mean_thick_mm
            outputField(str(sdCortSup1 * factor), True)  # Cortical_Sup1_sd_thick_mm
            outputField(str(minCortSup1 * factor), True)  # Cortical_Sup1_min_thick_mm
            outputField(str(maxCortSup1 * factor), True)  # Cortical_Sup1_max_thick_mm
            # Superior 1: Trabecular
            outputField(str(trabSup1BVTV), True)  # Trabecular_Sup1_BVTV
            outputField(str(meanTrabSup1 * factor), True)  # Trabecular_Sup1_mean_thick_mm
            outputField(str(sdTrabSup1 * factor), True)  # Trabecular_Sup1_sd_thick_mm
            outputField(str(minTrabSup1 * factor), True)  # Trabecular_Sup1_min_thick_mm
            outputField(str(maxTrabSup1 * factor), True)  # Trabecular_Sup1_max_thick_mm
            # Superior 1: Marrow
            outputField(str(meanMarrowSup1 * factor), True)  # Marrow_Sup1_mean_sep_mm
            outputField(str(sdMarrowsup1 * factor), True)  # Marrow_Sup1_sd_sep_mm
            outputField(str(minMarrowSup1 * factor), True)  # Marrow_Sup1_min_sep_mm
            outputField(str(maxMarrowSup1 * factor), True)  # Marrow_Sup1_max_sep_mm

            # Superior 2
            # Superior 2: Cortical
            outputField(str(cortSup2BVTV), True)  # Cortical_Sup2_BVTV
            outputField(str(meanCortSup2 * factor), True)  # Cortical_Sup2_mean_thick_mm
            outputField(str(sdCortSup2 * factor), True)  # Cortical_Sup2_sd_thick_mm
            outputField(str(minCortSup2 * factor), True)  # Cortical_Sup2_min_thick_mm
            outputField(str(maxCortSup2 * factor), True)  # Cortical_Sup2_max_thick_mm
            # Superior 2: Trabecular
            outputField(str(trabSup2BVTV), True)  # Trabecular_Sup2_BVTV
            outputField(str(meanTrabSup2 * factor), True)  # Trabecular_Sup2_mean_thick_mm
            outputField(str(sdTrabSup2 * factor), True)  # Trabecular_Sup2_sd_thick_mm
            outputField(str(minTrabSup2 * factor), True)  # Trabecular_Sup2_min_thick_mm
            outputField(str(maxTrabSup2 * factor), True)  # Trabecular_Sup2_max_thick_mm
            # Superior 2: Marrow
            outputField(str(meanMarrowSup2 * factor), True)  # Marrow_Sup2_mean_sep_mm
            outputField(str(sdMarrowsup2 * factor), True)  # Marrow_Sup2_sd_sep_mm
            outputField(str(minMarrowSup2 * factor), True)  # Marrow_Sup2_min_sep_mm
            outputField(str(maxMarrowSup2 * factor), True)  # Marrow_Sup2_max_sep_mm

            # Inferior 1
            # Inferior 1: Cortical
            outputField(str(CortInf1BVTV), True)  # Cortical_Inf1_BVTV
            outputField(str(meanCortInf1 * factor), True)  # Cortical_Inf1_mean_thick_mm
            outputField(str(sdCortInf1 * factor), True)  # Cortical_Inf1_sd_thick_mm
            outputField(str(minCortInf1 * factor), True)  # Cortical_Inf1_min_thick_mm
            outputField(str(maxCortInf1 * factor), True)  # Cortical_Inf1_max_thick_mm
            # Superior 1: Trabecular
            outputField(str(trabInf1BVTV), True)  # Trabecular_Inf1_BVTV
            outputField(str(meanTrabInf1 * factor), True)  # Trabecular_Inf1_mean_thick_mm
            outputField(str(sdTrabInf1 * factor), True)  # Trabecular_Inf1_sd_thick_mm
            outputField(str(minTrabInf1 * factor), True)  # Trabecular_Inf1_min_thick_mm
            outputField(str(maxTrabInf1 * factor), True)  # Trabecular_Inf1_max_thick_mm
            # Superior 1: Marrow
            outputField(str(meanMarrowInf1 * factor), True)  # Marrow_Inf1_mean_sep_mm
            outputField(str(sdMarrowInf1 * factor), True)  # Marrow_Inf1_sd_sep_mm
            outputField(str(minMarrowInf1 * factor), True)  # Marrow_Inf1_min_sep_mm
            outputField(str(maxMarrowInf1 * factor), True)  # Marrow_Inf1_max_sep_mm

            # Inferior 2
            # Inferior 2: Cortical
            outputField(str(CortInf2BVTV), True)  # Cortical_Inf1_BVTV
            outputField(str(meanCortInf2 * factor), True)  # Cortical_Inf2_mean_thick_mm
            outputField(str(sdCortInf2 * factor), True)  # Cortical_Inf2_sd_thick_mm
            outputField(str(minCortInf2 * factor), True)  # Cortical_Inf2_min_thick_mm
            outputField(str(maxCortInf2 * factor), True)  # Cortical_Inf2_max_thick_mm
            # Inferior 2: Trabecular
            outputField(str(trabInf2BVTV), True)  # Trabecular_Inf1_BVTV
            outputField(str(meanTrabInf2 * factor), True)  # Trabecular_Inf2_mean_thick_mm
            outputField(str(sdTrabInf2 * factor), True)  # Trabecular_Inf2_sd_thick_mm
            outputField(str(minTrabInf2 * factor), True)  # Trabecular_Inf2_min_thick_mm
            outputField(str(maxTrabInf2 * factor), True)  # Trabecular_Inf2_max_thick_mm
            # Inferior 2: Marrow
            outputField(str(meanMarrowInf2 * factor), True)  # Marrow_Inf2_mean_sep_mm
            outputField(str(sdMarrowInf2 * factor), True)  # Marrow_Inf2_sd_sep_mm
            outputField(str(minMarrowInf2 * factor), True)  # Marrow_Inf2_min_sep_mm
            outputField(str(maxMarrowInf2 * factor), True)  # Marrow_Inf2_max_sep_mm

            outputEOL()

            print('Finished writing to results file...')

            # Closing the file
            fio.close()

            # Delete unnecessary/temp ROIs, Channels, arrays, etc...
            aROIC.deleteObject()
            aROISG.deleteObject()
            aTotalROI.deleteObject()
        else:
           print("3D Quadrent Properties were not calculated")
           aCortVolumeThicknessChannel = Channel()


        if bCalcCorticalSlice:
            progress.setExtraText('Running Cortical Slice Results...')
            print('Calling function to CalculateCortical Slice Properites...')
            calcCorticalSliceProps(cls, boneROI, corticalROI, marrowROI, foldername, aCortVolumeThicknessChannel,
                                   bCalc3DQuad, zslicePadding)
            print('Returned from function to CalculateCortical Slice Properites...')

        print(' ')
        print('*****FINISHED******')
        print(' ')

        # Closing and deletion of the progress object
        aCortVolumeThicknessChannel.deleteObject()
        progress.deleteObject()

        return

def calcCorticalSliceProps(cls, boneROI, corticalROI, marrowROI, foldername, aCortVolumeThicknessChannel, bCalc3DQuad,
                           zslicePadding):
    """
    Calculates Cortical Slice properties

    :param boneROI: Bone ROI
    :type boneROI: ORSModel.ors.ROI
    :param corticalROI: Cortical ROI
    :type corticalROI: ORSModel.ors.ROI
    :param marrowROI: Marrow ROI
    :type marrowROI: ORSModel.ors.ROI
    :param foldername: the folder to save the results into
    :type foldername: folder saving
    :param aCortVolumeThicknessChannel: Cortical volume thickness channel
    :type aCortVolumeThicknessChannel: ORSModel.ors.Channel
    :param bCalc3DQuad: flag to calculate Cortical slice properties
    :type bCalc3DQuad: bool
    :param zslicePadding: amount of z-slices to pad in the z-direction
    :type zslicePadding: int
    """
    print(' ')
    print('In function to CalculateCortical Slice Properites...')
    print('  The folder name for saving results is: ', foldername)

    # Getting the total voxel count for each ROI
    print('  The total voxel count of Bone: ', boneROI.getVoxelCount(0))
    print('  The total voxel count of Cortical: ', corticalROI.getVoxelCount(0))
    print('  The total voxel count of Marrow: ', marrowROI.getVoxelCount(0))

    aTotalROI = corticalROI.copy()
    aTotalROI.addROI(marrowROI)
    print('  The total voxel count of Total ROI: ', aTotalROI.getVoxelCount(0))

    #  x, y, and z dimensions
    xSize = aTotalROI.getXSize()
    ySize = aTotalROI.getYSize()
    zSize = aTotalROI.getZSize()
    print('  The xSize is: ', xSize)
    print('  The ySize is: ', ySize)
    print('  The zSize for a Total ROI is: ', zSize)

    # Create a structured grid for all ROIs for slice results
    aROISG = ROIHelper.createFullVolumeROIWithStructuredGrid(aTotalROI)
    aCortROISG = ROIHelper.createFullVolumeROIWithStructuredGrid(corticalROI)
    aMarrowROISG = ROIHelper.createFullVolumeROIWithStructuredGrid(marrowROI)

    # Find the dimensions and save the z-dimension of the Structured Grid
    xSpacing = aROISG.getXSpacing()
    ySpacing = aROISG.getYSpacing()
    zSpacing = aROISG.getZSpacing()
    print('  The xSize is: ', xSpacing)
    print('  The ySize is: ', ySpacing)
    print('  The zSize is: ', zSpacing)

    # Allocate arrays for each property calculating so we can calculate SD in addition to average variable
    aTtAr = zeros([zSize])
    aCtAr = zeros([zSize])
    aMaAr = zeros([zSize])
    aCtTh = zeros([zSize])
    xGCentroidP = zeros([zSize])
    xGCentroidCS = zeros([zSize])
    xGCentroidM = zeros([zSize])
    yGCentroidP = zeros([zSize])
    yGCentroidCS = zeros([zSize])
    yGCentroidM = zeros([zSize])
    periostealPerim = zeros([zSize])
    endocorticalPerim = zeros([zSize])
    totalBVF = zeros([zSize])
    corticalBVF = zeros([zSize])
    marrowBVF = zeros([zSize])
    ixx = zeros([zSize])
    ixy = zeros([zSize])
    iyy = zeros([zSize])
    imin = zeros([zSize])
    imax = zeros([zSize])
    polari = zeros([zSize])
    polari2 = zeros([zSize])

    # Create a Cortical Volume thickness map for slice by slice results
    currentTime = 0
    # aCortVolumeThicknessChannel is passed because this is the most time consuming step in our code. If calculated
    # for 3-D measures, use, if not, we need to create the 3-D volume thickness map
    if bCalc3DQuad:
       aCortVolumeThicknessChannel = aCortVolumeThicknessChannel
    else:
        if zslicePadding == 0:
            aCortVolumeThicknessChannel = OrsVolumeROITools.createVolumeThicknessFromROI(corticalROI,
                                                                                         currentTime=currentTime,
                                                                                         IProgress=None)
        else:
            paddedCortROI = corticalROI.copy()
            # paddedCortROISG = ROIHelper.createFullVolumeROIWithStructuredGrid(paddedCortROI)
            orig_zsize = corticalROI.getZSize()
            padded_zsize = orig_zsize + (2 * zslicePadding)
            paddedCortROI.setZSize(padded_zsize)
            box_paddedCortROISG = paddedCortROI.getBox()
            paddedCortROISG_direction2 = box_paddedCortROISG.getDirection2()
            paddedCortROISG_spacingdirection2 = box_paddedCortROISG.getDirection2Spacing()
            paddedCortROISG_origin = box_paddedCortROISG.getOrigin()
            paddedCortROISG_neworigin = paddedCortROISG_origin - (zslicePadding * paddedCortROISG_spacingdirection2
                                                                  * paddedCortROISG_direction2)
            box_paddedCortROISG.setOrigin(paddedCortROISG_neworigin)
            paddedCortROI.setBox(box_paddedCortROISG)
            paddedCortROI.clearROI()
            # paddedCortROISG.clearROI()
            timeStep = 0
            # Copy the common region data
            paddedCortROI.addROI(corticalROI)

            # Padding at the lower z
            tempROILowerZ = corticalROI.getSubset(0, 0, 0, timeStep, paddedCortROI.getXSize() - 1,
                                                  paddedCortROI.getYSize() - 1, 0, timeStep, None, None)

            for zi in range(zslicePadding):
                originToSet = paddedCortROI.getVoxelToWorldCoordinates(orsVect(0, 0, zi))
                tempROILowerZ.setOrigin(originToSet)
                paddedCortROI.addROI(tempROILowerZ)
            tempROILowerZ.deleteObject()

            # Padding at the higher z
            tempROIHigherZ = corticalROI.getSubset(0, 0, orig_zsize - 1, timeStep, paddedCortROI.getXSize() - 1,
                                                   paddedCortROI.getYSize() - 1, orig_zsize - 1, timeStep, None, None)
            for zi in range(zslicePadding):
                originToSet = paddedCortROI.getVoxelToWorldCoordinates(orsVect(0, 0, padded_zsize - 1 - zi))
                tempROIHigherZ.setOrigin(originToSet)
                paddedCortROI.addROI(tempROIHigherZ)
            tempROIHigherZ.deleteObject()

            paddedCortROI.setTitle(corticalROI.getTitle() + 'Padded')
            # paddedCortROI.publish()

            aCortVolumeThicknessChannel = OrsVolumeROITools.createVolumeThicknessFromROI(paddedCortROI,
                                                                                         currentTime=currentTime,
                                                                                         IProgress=None)
            paddedCortROI.deleteObject()
    # aCortVolumeThicknessChannel.publish()

    # Loop over zslices
    print('  Now Calculating slice properties')
    for iz in range(0, zSize):
    #for iz in range(0, 3):
        print('    On slice iz = ', iz)
        # Total ROI (Cortical + Marrow)
        # We keep getting incorrect center of mass indexing so I am printing the center of mass and voxel center of
        # mas at the beginnign of the loop to see if this is where the problem is occuring
        copytotalROI = aTotalROI.copy()
        sliceROItotal = copytotalROI.getAsROIClipped(0, 0, iz, 0, (xSize - 1), (ySize - 1), iz, 0, copytotalROI)
        sliceROItotal.setTitle('total ROI in loop')
        # sliceROItotal.publish()

        # Cortical ROI
        copycorticalROI = corticalROI.copy()
        sliceROIcortical = copycorticalROI.getAsROIClipped(0, 0, iz, 0, (xSize - 1), (ySize - 1), iz, 0,
                                                           copycorticalROI)
        sliceROIcortical.setTitle('Cortical ROI in loop')


        # Marrow ROI
        copymarrowROI = marrowROI.copy()
        sliceROImarrow = copymarrowROI.getAsROIClipped(0, 0, iz, 0, (xSize - 1), (ySize - 1), iz, 0, copymarrowROI)
        sliceROImarrow.setTitle('Marrow ROI in loop')
        # sliceROImarrow.publish()


        # Calculates ROI Areas (1-3)
        aTtAr[iz] = sliceROItotal.getVoxelCount(0)
        aCtAr[iz] = sliceROIcortical.getVoxelCount(0)
        aMaAr[iz] = sliceROImarrow.getVoxelCount(0)

        # Calculates Cortical Thickness (4)
        aCtTh[iz] = ROI.getMeanSourceDataValue(sliceROIcortical, currentTime, aCortVolumeThicknessChannel)

        # Calculates the area moments of inertia is the bottom code (5)
            # Done after finding bv/tv as need centroid and roi's calculated for properties 6-9...

        # Calculates Periosteal Perimeter (6)
        vCenterMass = sliceROItotal.getCenterOfMass(0)
        print('      Calculating Periosteal perim...')
        print('      The ROI total (Cortical + Marrow) center of mass is: ', vCenterMass)
        # Define 3 points for plane, point1 is centroid position and then point0 & point2 are moved
        # in the X or Y direction from the centroid
        point1 = vCenterMass.copy()
        point0 = vCenterMass.copy()
        point2 = vCenterMass.copy()
        # print('      The type of point1: ', type(point1))
        # print('      The values of point1: ', point1)
        # print('      The initial values of point0: ', point0)
        # print('      The initial values of point2: ', point2)
        point1X = point1.getX()
        point1Y = point1.getY()
        point1Z = point1.getZ()
        # print('        point1-X: ', point1X)
        # print('        point1-Y: ', point1Y)
        # print('        point1-Z: ', point1Z)
        # point0.setXYZ((point1X-(point1X/4)), point1Y, point1Z)
        point0.setX(point1X-(point1X/4))
        # point1.setXYZ(voxCenterMass[0] + 2, voxCenterMass[1], voxCenterMass[2])
        # point2.setXYZ(point1X, (point1Y-(point1Y/4)), point1Z)
        point2.setY(point1Y-(point1Y/4))
        # print('      The reset values of point0: ', point0)
        # print('      The reset values of point2: ', point2)
        periosteal_plane = Plane()
        periosteal_plane.from3Points(point0, point1, point2)
        periostealPerim[iz] = aTotalROI.getTotalPerimeterOnPlane(periosteal_plane, 0)
        # print('      The periosteal perimeter is: ', str(periostealPerim[iz]))
        # print(' ')

        # Calculates Endocortical Perimeter (7)
        vCenterMassMar = sliceROImarrow.getCenterOfMass(0)
        # print('      Calculating Endosteal perim...')
        # print('      The type of the center of mass, vCenterMassMar, is: ', type(vCenterMassMar))
        print('      The marrow ROI Center of Mass is: ', vCenterMassMar)
        # Define 3 points for plane, point1 is centroid position and then point0 & point2 are moved
        # in the X or Y direction from the centroid
        point1Ec = vCenterMassMar.copy()
        point1Ec.setZ(point1.getZ())
        point0Ec = vCenterMassMar.copy()
        point0Ec.setZ(point1.getZ())
        point2Ec = vCenterMassMar.copy()
        point2Ec.setZ(point1.getZ())
        # print('      The type of point1: ', type(point1Ec))
        # print('      The values of point1: ', point1Ec)
        # print('      The initial values of point0: ', point0Ec)
        # print('      The initial values of point2: ', point2Ec)
        point1XEc = point1Ec.getX()
        point1YEc = point1Ec.getY()
        point1ZEc = point1Ec.getZ()
        # print('        point1-X: ', point1XEc)
        # print('        point1-Y: ', point1YEc)
        # print('        point1-Z: ', point1ZEc)
        # point0.setXYZ((point1X-(point1X/4)), point1Y, point1Z)
        point0Ec.setX(point1XEc - (point1XEc / 4))
        # point1.setXYZ(voxCenterMass[0] + 2, voxCenterMass[1], voxCenterMass[2])
        # point2.setXYZ(point1X, (point1Y-(point1Y/4)), point1Z)
        point2Ec.setY(point1YEc - (point1YEc / 4))
        # print('      The reset values of point0: ', point0Ec)
        # print('      The reset values of point2: ', point2Ec)
        endocortical_plane = Plane()
        endocortical_plane.from3Points(point0Ec, point1Ec, point2Ec)
        endocorticalPerim[iz] = sliceROImarrow.getTotalPerimeterOnPlane(endocortical_plane, 0)
        # print('      The endocortical perimeter is: ', str(endocorticalPerim[iz]))
        # print(' ')

        # Calculates Bone volume within the region of interest (8)
        # Total BVF
        boneIntTotal = boneROI.getIntersectionWithROI(sliceROItotal, None)
        totalBVF[iz] = ROI.getTotalVoxelCount(boneIntTotal) / ROI.getTotalVoxelCount(sliceROItotal)  # exported value
        # Cortical BVF
        boneIntCort = boneROI.getIntersectionWithROI(sliceROIcortical, None)
        corticalBVF[iz] = ROI.getTotalVoxelCount(boneIntCort) / ROI.getTotalVoxelCount(sliceROIcortical)  # exported value
        # Marrow BVF
        boneIntMarr = boneROI.getIntersectionWithROI(sliceROImarrow, None)
        marrowBVF[iz] = ROI.getTotalVoxelCount(boneIntMarr) / ROI.getTotalVoxelCount(sliceROImarrow)  # exported value

        # Calculates Geometric Centroid in voxels (9)
        # Total ROI Centroid  - Periosteal Area
        # convert ROI from single slice to structured grid
        singleSliceSG = ROIHelper.createFullVolumeROIWithStructuredGrid(sliceROItotal)
        voxCenterMass = StructuredGrid.getWorldToVoxelCoordinates(singleSliceSG, vCenterMass)
        print('      The Total ROI (Cortical + Marrow) voxCenterMass is: ', voxCenterMass)
        # print('      Voxel Center of mass for Total ROI: ', voxCenterMass)
        xGCentroidP[iz] = voxCenterMass[0]
        yGCentroidP[iz] = voxCenterMass[1]

        # Cortical ROI Centroid  - Cortical Shell
        singleSliceSGCort = ROIHelper.createFullVolumeROIWithStructuredGrid(sliceROIcortical)
        vCenterMassCort = sliceROIcortical.getCenterOfMass(0)
        voxCenterMassCort = StructuredGrid.getWorldToVoxelCoordinates(singleSliceSG, vCenterMassCort)
        print('      Voxel Center of mass for Cortical ROI: ', voxCenterMassCort)
        xGCentroidCS[iz] = voxCenterMassCort[0]
        yGCentroidCS[iz] = voxCenterMassCort[1]

        # Cortical ROI Centroid  - Marrow Area
        singleSliceSGMar = ROIHelper.createFullVolumeROIWithStructuredGrid(sliceROImarrow)
        voxCenterMassMar = StructuredGrid.getWorldToVoxelCoordinates(singleSliceSGMar, vCenterMassMar)
        print('      Voxel Center of mass for Marrow ROI: ', voxCenterMassMar)
        xGCentroidM[iz] = voxCenterMassMar[0]
        yGCentroidM[iz] = voxCenterMassMar[1]

        # Calculates the area moments of inertia is the bottom code (5)
        # moment of inertia calculated from the centroid of the cortex; sum over threhold voxels only
        # Take intersection of BoneROI and CortROI to get just the bone voxels on current slice in the cortical ROI
          # calculated previously as "boneIntCort"
        # From this ROI, get the x & y index position of each voxel that is bone.
        # chBoneIntCort = Channel()
        chBoneIntCort = boneIntCort.convertToChannel(255)
        # chBoneIntCort.publish()
        npBoneIntCort = chBoneIntCort.getNDArray(0)
        #print('       min value of npBoneIntCort = ', npBoneIntCort.min())
        #print('       max value of npBoneIntCort = ', npBoneIntCort.max())
        idx_cortBone = np.where(npBoneIntCort != 0)
        # print('    index of bone voxels in cortBone array:')
        # print(idx_cortBone)
        # The coordinates in idx_cortBone are as z,y,x
        idx_cortBoneX = idx_cortBone[2] * xSpacing
        idx_cortBoneY = idx_cortBone[1] * ySpacing
        # print('       X coordinates:')
        # print(idx_cortBoneX)
        # print('       Y coordinates:')
        # print(idx_cortBoneY)

        # Get centroid of cortical ROI in voxels values
        singleSliceSGboneIntCort = ROIHelper.createFullVolumeROIWithStructuredGrid(boneIntCort)
        vCenterMassboneIntCort = boneIntCort.getCenterOfMass(0)
        voxCenterMassboneIntCort = StructuredGrid.getWorldToVoxelCoordinates(singleSliceSGboneIntCort, vCenterMassboneIntCort)
        xGCentroidBC = voxCenterMassboneIntCort[0] * xSpacing
        yGCentroidBC = voxCenterMassboneIntCort[1] * ySpacing
        print(' The centroid of the bone in the cortical ROI only is: ', voxCenterMassboneIntCort)

        # Get cortical area of the bone-cort ROI intersection...
        boneIntCortArea = boneIntCort.getVoxelCount(0) * xSpacing * ySpacing
        # print('     boneIntCort area = ', boneIntCortArea)
        # Now calculate squared and sum of the coordinates needed to calculated the Moments of Inertia(s)
        idx_cortBoneX_2 = idx_cortBoneX**2
        sum_idx_cortBoneX_2 = sum(idx_cortBoneX_2)

        idx_cortBoneY_2 = idx_cortBoneY**2
        sum_idx_cortBoneY_2 = sum(idx_cortBoneY_2)

        idx_cortBoneXY = idx_cortBoneX * idx_cortBoneY
        sum_idx_cortBoneXY = sum(idx_cortBoneXY)

        # Moment of Inertia ixx
        ixx[iz] = (sum_idx_cortBoneY_2*xSpacing*ySpacing) - (boneIntCortArea * ((yGCentroidBC*ySpacing)**2))
        # Moment of Inertia iyy
        iyy[iz] = (sum_idx_cortBoneX_2*xSpacing*ySpacing) - (boneIntCortArea * ((xGCentroidBC*xSpacing)**2))
        # Moment of Inertia ixy
        ixy[iz] = (sum_idx_cortBoneXY*xSpacing*ySpacing) - (boneIntCortArea * (yGCentroidBC * xGCentroidBC *
                                                                            xSpacing * ySpacing))
        # Minimum moment of inertia
        imin[iz] = ((ixx[iz] + iyy[iz])/2) + (((ixx[iz] - iyy[iz])/2)**2 + ixy[iz]**2)**(1/2)
        # Maximum moment of inertia
        imax[iz] = ((ixx[iz] + iyy[iz])/2) - (((ixx[iz] - iyy[iz])/2)**2 + ixy[iz]**2)**(1/2)

        # Deleting Objects
        copytotalROI.deleteObject()
        sliceROItotal.deleteObject()
        copycorticalROI.deleteObject()
        sliceROIcortical.deleteObject()
        copymarrowROI.deleteObject()
        sliceROImarrow.deleteObject()
        singleSliceSG.deleteObject()
        singleSliceSGMar.deleteObject()
        boneIntTotal.deleteObject()
        boneIntCort.deleteObject()
        boneIntMarr.deleteObject()
        singleSliceSGCort.deleteObject()
        singleSliceSGboneIntCort.deleteObject()
        chBoneIntCort.deleteObject()

    # Convert this to area using the x and y voxel size (in mm)
    aTtAr = aTtAr * ySpacing * xSpacing * 1000 * 1000
    aCtAr = aCtAr * ySpacing * xSpacing * 1000 * 1000
    aMaAr = aMaAr * ySpacing * xSpacing * 1000 * 1000
    aCtTh = aCtTh * 1000
    periostealPerim = periostealPerim * 1000
    endocorticalPerim = endocorticalPerim * 1000
    # moments of inertia are to the 4th power so need to multiple 1000^4
    ixx = ixx * (1000 ** 4)
    iyy = iyy * (1000 ** 4)
    ixy = ixy * (1000 ** 4)
    imin = imin * (1000 ** 4)
    imax = imax * (1000 ** 4)
    # polar moment of inertia
    polari = imin + imax
    polari2 = ixx + iyy

    # Calculate Means & SD's
    meanaTtAr = aTtAr.mean()
    sdaTtAr = aTtAr.std()
    meanaCtAr = aCtAr.mean()
    sdaCtAr = aCtAr.std()
    meanaMaAr = aMaAr.mean()
    sdaMaAr = aMaAr.std()
    meanasCtTh = aCtTh.mean()
    sdaCtTh = aCtTh.std()
    meanperiostealPerim = periostealPerim.mean()
    sdperiostealPerim = periostealPerim.std()
    meanendocorticalPerim = endocorticalPerim.mean()
    sdendocorticalPerim = endocorticalPerim.std()
    meanxGCentroidP = xGCentroidP.mean()
    sdxGCentroidP = xGCentroidP.std()
    meanyGCentroidP = yGCentroidP.mean()
    sdyGCentroidP = yGCentroidP.std()
    meanxGCentroidCS = xGCentroidCS.mean()
    sdxGCentroidCS = xGCentroidCS.std()
    meanyGCentroidCS = yGCentroidCS.mean()
    sdyGCentroidCS = yGCentroidCS.std()
    meanxGCentroidM = xGCentroidM.mean()
    sdxGCentroidM = xGCentroidM.std()
    meanyGCentroidM = yGCentroidM.mean()
    sdyGCentroidM = yGCentroidM.std()
    meantotalBVF = totalBVF.mean()
    sdtotalBVF = totalBVF.std()
    meancorticalBVF = corticalBVF.mean()
    sdcorticalBVF = corticalBVF.std()
    meanmarrowBVF = marrowBVF.mean()
    sdmarrowBVF = marrowBVF.std()
    meanixx = ixx.mean()
    sdixx = ixx.std()
    meanixy = ixy.mean()
    sdixy = ixy.std()
    meaniyy = iyy.mean()
    sdiyy = iyy.std()
    meanimin = imin.mean()
    sdimin = imin.std()
    meanimax = imax.mean()
    sdimax = imax.std()
    meanpolari = polari.mean()
    sdpolari = polari.std()
    meanpolari2 = polari2.mean()
    sdpolari2 = polari2.std()
    # Write out results to CSV file(s)
    print(' About to write results to output file...')

    print('The Average Results')
    outputfilenameAveSS = str(foldername) + '/' + str(ROI.getTitle(boneROI)) + 'Average_Single_Slice.csv'
    print('The title of BoneROI is: ', outputfilenameAveSS)
    # csv delimiter
    delimiter = ','
    # Opening the file
    try:
        fio = open(outputfilenameAveSS, "w")
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
    columnNames = ["Title ROI", "Units", "Slices", "TtAr_mean", "TtAr_sd", "CtAr_mean", "CtAr_sd", "MaAr_mean", "MaAr_sd",
                   "CtTh_mean", "CtTh_sd", "x_mean_Periosteal_GC_vox", "x_sd_Periosteal_GC_vox",
                   "y_mean_Periosteal_GC_vox", "y_sd_Periosteal_GC_vox", "x_mean_CortShell_GC_vox",
                   "x_sd_CortShell_GC_vox", "y_mean_CortShell_GC_vox", "y_sd_CortShell_GC_vox",
                   "x_mean_Ma.Ar_GC_vox", "x_sd_Ma.Ar_GC_vox", "y_mean_Ma.Ar_GC_vox", "y_sd_Ma.Ar_GC_vox",
                   "Ps.Perim_mean", "Ps.Perim_sd", "Ec.Perim_mean", "Ec.Perim.sd", "Total_BVF_mean", "Total_BFV_sd",
                   "Cortical_BVF_mean", "Cortical_BVF_sd", "Marrow_BVF_mean", "Marrow_BVF_sd", "ixx_mean","ixx_sd",
                   "ixy_mean", "ixy_sd", "iyy_mean", "iyy_sd", "imin_mean", "imin_sd", "imax_mean", "imax_sd",
                   "polari_mean", "polari_sd", "polari2_mean", "polari2_sd"]

    print(' About to write results to output file...')
    for field in columnNames[:-1]:
        outputField(field, True)
    outputField(columnNames[-1], False)
    outputEOL()
    # Average Values
    outputField(boneROI.getTitle(), True)
    outputField("mm", True)
    outputField(str(zSize), True)
    outputField(str(meanaTtAr), True)
    outputField(str(sdaTtAr), True)
    outputField(str(meanaCtAr), True)
    outputField(str(sdaCtAr), True)
    outputField(str(meanaMaAr), True)
    outputField(str(sdaMaAr), True)
    outputField(str(meanasCtTh), True)
    outputField(str(sdaCtTh), True)
    outputField(str(meanxGCentroidP), True)
    outputField(str(sdxGCentroidP), True)
    outputField(str(meanyGCentroidP), True)
    outputField(str(sdyGCentroidP), True)
    outputField(str(meanxGCentroidCS), True)
    outputField(str(sdxGCentroidCS), True)
    outputField(str(meanyGCentroidCS), True)
    outputField(str(sdyGCentroidCS), True)
    outputField(str(meanxGCentroidM), True)
    outputField(str(sdxGCentroidM), True)
    outputField(str(meanyGCentroidM), True)
    outputField(str(sdyGCentroidM), True)
    outputField(str(meanperiostealPerim), True)
    outputField(str(sdperiostealPerim), True)
    outputField(str(meanendocorticalPerim), True)
    outputField(str(sdendocorticalPerim), True)
    outputField(str(meantotalBVF), True)
    outputField(str(sdtotalBVF), True)
    outputField(str(meancorticalBVF), True)
    outputField(str(sdcorticalBVF), True)
    outputField(str(meanmarrowBVF), True)
    outputField(str(sdmarrowBVF), True)
    outputField(str(meanixx), True)
    outputField(str(sdixx), True)
    outputField(str(meanixy), True)
    outputField(str(sdixy), True)
    outputField(str(meaniyy), True)
    outputField(str(sdiyy), True)
    outputField(str(meanimin), True)
    outputField(str(sdimin), True)
    outputField(str(meanimax), True)
    outputField(str(sdimax), True)
    outputField(str(meanpolari), True)
    outputField(str(sdpolari), True)
    outputField(str(meanpolari2), True)
    outputField(str(sdpolari2), True)


    print('The single slice results')
    outputfilenameSS = str(foldername) + '/' + str(ROI.getTitle(boneROI)) + 'Single_Slice.csv'
    print('The title of BoneROI is: ', outputfilenameSS)
    df = pd.DataFrame({"TtAr": aTtAr, "CtAr": aCtAr, "MaAr": aMaAr, "CtTh": aCtTh, "Geometric_Centroid_P.Ar_x": xGCentroidP,
                       "Geometric_Centroid_P.Ar_y": yGCentroidP, "Geometric_Centroid_CS.Ar_x": xGCentroidCS,
                       "Geometric_Centroid_CS.Ar_y": yGCentroidCS, "Geometric_Centroid_Ma.Ar_x": xGCentroidM,
                       "Geometric_Centroid_Ma.Ar_y": yGCentroidM, "Ps.Perim": periostealPerim,
                       "Ec.Perim": endocorticalPerim, "Tot.BVF": totalBVF, "Cort.BVF":corticalBVF, "Mar.BVF": marrowBVF,
                       "ixx": ixx, "ixy": ixy, "iyy": iyy, "imin": imin, "imax": imax, "Polari": polari, "Polari2": polari2})
    df.to_csv(outputfilenameSS, index=False)

    # Clean up/delete temp objects/arrays created
    aTotalROI.deleteObject()
    aROISG.deleteObject()
    aCortROISG.deleteObject()
    aMarrowROISG.deleteObject()
    aCortVolumeThicknessChannel.deleteObject()

    # Done...
    return

