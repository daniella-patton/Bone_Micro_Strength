"""
This plugin is used to 'average' three ROIs to create a Ground Truth ROI.

The GT ROI is created by setting a voxel as ON if it is on in 2 or more of
the three input ROIs, otherwise it is set to OFF. The plugin will check to
make sure all three input ROI's exist and are the same shape. The GT ROI will
have the same shape as the input ROIs, and will be associated with the same
input image as ROI-1.

:author: Daniella Patton and Rob Goulet
:contact:
:email: pattondm@umich.edu; rgoulet@med.umich.edu
:organization: University of Michigan - Department of Orthopeadic Surgery
:address: 102 Zina Pitcher Place
:copyright: 2019
:date: Feb 05 2019 09:03
:dragonflyVersion: 4.0.0.569
:UUID: d7417746294e11e9a4db005056c00008
"""

__version__ = '1.0.0'

from OrsLibraries.workingcontext import WorkingContext
from ORSServiceClass.OrsPlugin.orsPlugin import OrsPlugin
from ORSServiceClass.decorators.infrastructure import interfaceMethod, menuItem
from ORSServiceClass.actionAndMenu.menu import Menu
from ORSServiceClass.OrsPlugin.uidescriptor import UIDescriptor
from .mainform import MainForm

from ORSModel import ROI, orsColor


class Ground_Truth_ROI_d7417746294e11e9a4db005056c00008(OrsPlugin):

    # Plugin definition
    multiple = True
    closable = True
    savable = False
    keepAlive = False

    # UIs
    UIDescriptors = [UIDescriptor(name='MainForm',
                                  title='Create Ground Truth ROI',
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
        instance = Ground_Truth_ROI_d7417746294e11e9a4db005056c00008()
        if instance is not None:
            instance.openWidget('MainForm')

    @classmethod
    @menuItem('ORL')
    def GroundTruthROICreation(cls):
        aMenuItem = Menu(title='Create Ground Truth',
                         id_='Ground_Truth_ROI_d7417746294e11e9a4db005056c00008_1',
                         section='',
                         action='Ground_Truth_ROI_d7417746294e11e9a4db005056c00008.openGUI()')
        return aMenuItem

    @classmethod
    @interfaceMethod
    def GroundTruthROI(cls, aROI1, aROI2, aROI3, aGTName):
        """
        Computes and average ROI from three input ROIS

        :param aROI1: input ROI1
        :type aROI1: ORSModel.ors.ROI
        :param aROI2: input ROI2
        :type aROI2: ORSModel.ors.ROI
        :param aROI3: input ROI3
        :type aROI3: ORSModel.ors.ROI
        :param aGTName: name of new Ground Truth ROI
        :type aGTName: str
        """
        # Make sure that the input ROIS exist and are of the same size
        print('Checking if valid ROIS')
        if aROI1 is None:
            return
        if aROI2 is None:
            return
        if aROI3 is None:
            return
        print('Checking if size is equal')
        if not aROI1.getHasSameShape(aROI2):
            return
        if not aROI1.getHasSameShape(aROI3):
            return

        # Creating a Channel from the ROIs
        aROI1_channel = aROI1.convertToChannel(1)
        aROI2_channel = aROI2.convertToChannel(1)
        aROI3_channel = aROI3.convertToChannel(1)
        aGT_channel = aROI1_channel.copy()
        print('Created channels for input and GT ROIs')

        # Create and array of numbers from the channel to manipulate
        aGT_channel_ndarray = aGT_channel.getNDArray()
        aROI2_channel_ndarray = aROI2_channel.getNDArray()
        aROI3_channel_ndarray = aROI3_channel.getNDArray()

        # Add the arrays together so that we have a range of values 0-3
        aGT_channel_ndarray[:, :, :] = aGT_channel_ndarray[:, :, :] + aROI2_channel_ndarray[:, :, :] + aROI3_channel_ndarray[:, :, :]
        print('Summed 3 input arrays together..')

        # Create the final ROI from the summed ROI's that was on in at least 2 (or 3) of the three ROI's. As want the
        # whole ROI, using .getAsROIWithinRange() and not .getAsROIWithinRangeInArea() where you need to specify the
        # min/max dimensions of ROI to get.
        aGTROI = ROI()
        aGTROI.setInitialColor(orsColor(1, 0, 0, 1))     # Set as Red
        aGTROI.copyShapeFromStructuredGrid(aGT_channel)  # Make same shape/size of input ROI's
        # aGT_channel.publish()
        # print('Published the GT_channel')
        aGT_channel.getAsROIWithinRange(2, 3, None, aGTROI)
        print('Set GT ROI within range or 2-3...')
        aGTROI.setTitle(str(aGTName))
        print('Get GT new title to ', str(aGTName))
        aGTROI.publish()
        print('Published the new GT ROI')

        # Delete all temp objects created
        aROI1_channel.deleteObject()
        aROI2_channel.deleteObject()
        aROI3_channel.deleteObject()
        aGT_channel.deleteObject()
        del aROI2_channel_ndarray
        del aROI3_channel_ndarray

        print('Deleted temp ROIs and ndarrays created...')

        return
