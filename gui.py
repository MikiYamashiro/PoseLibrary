import os
import shiboken
from PySide import QtCore, QtGui
from PySide.QtUiTools import QUiLoader
from maya import OpenMayaUI
from . import function as fnc
from . import Define


def getMayaMainWindow():
    maya_ptr = OpenMayaUI.MQtUtil_mainWindow()
    return shiboken.wrapInstance(maya_ptr, QtGui.QMainWindow)


class GUI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(getMayaMainWindow())
        loader = QUiLoader()
        uiFilePath = os.path.join(os.path.dirname(__file__), 'PoseLibrary.ui')
        self.UI = loader.load(uiFilePath)
        self.setCentralWidget(self.UI)
        self.setWindowTitle(Define.WINDOW_TITLE)
        self.setObjectName(Define.WINDOW_NAME)
        self.resize(510, 750)
        self.__setui()
        self.__setSlots()

    def __setui(self):
        assetlist = fnc.searchAssetName()
        for asset in assetlist:
            if os.path.isdir:
                if not asset == ".DS_Store":
                    self.UI.asset_comboBox.addItem(asset)
                    self.UI.load_comboBox.addItem(asset)

        asset_name = self.UI.load_comboBox.currentText()
        posedict = fnc.searchPoseList(asset_name)
        self.UI.pose_listWidget.setViewMode(QtGui.QListView.IconMode)
        self.UI.pose_listWidget.setIconSize(QtCore.QSize(200, 200))

        for (k, v) in posedict.items():
            self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon(v),str(k)))

    def __setSlots(self):
        self.UI.filedialog_pushButton.clicked.connect(self.openFileDialog)
        self.UI.pathset_pushButton.clicked.connect(self.setDirPath)
        self.UI.entry_pushButton.clicked.connect(self.assetEntryWindow)
        self.UI.save_pushButton.clicked.connect(self.poseSave)
        self.UI.delete_pushButton.clicked.connect(self.assetDelete)
        self.UI.load_pushButton.clicked.connect(self.poseLoad)
        self.UI.load_comboBox.currentIndexChanged.connect(self.loadName)

    def openFileDialog(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, "Select Save Path", "",False)
        self.UI.pathtext_lineEdit.setText(path)

    def setDirPath(self):
        print "setDirPath"
        Define.DATAUPPATH = self.UI.pathtext_lineEdit.text()
        print Define.DATAUPPATH

        assetlist = fnc.searchAssetName()
        for asset in assetlist:
            if os.path.isdir:
                if not asset == ".DS_Store":
                    self.UI.asset_comboBox.addItem(asset)
                    self.UI.load_comboBox.addItem(asset)

        asset_name = self.UI.load_comboBox.currentText()
        posedict = fnc.searchPoseList(asset_name)
        self.UI.pose_listWidget.setViewMode(QtGui.QListView.IconMode)
        self.UI.pose_listWidget.setIconSize(QtCore.QSize(200, 200))

        for (k, v) in posedict.items():
            self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon(v),str(k)))


    def loadName(self):
        self.UI.pose_listWidget.clear()
        asset_name = self.UI.load_comboBox.currentText()
        posedict = fnc.searchPoseList(asset_name)
        for (k, v) in posedict.items():
            self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon(v), str(k)))

    def assetEntryWindow(self):
        asset_name = self.UI.asset_lineEdit.text()
        fnc.assetSetUp(asset_name)
        # Add Items ComboBox
        self.UI.asset_comboBox.addItem(asset_name)
        self.UI.load_comboBox.addItem(asset_name)

    def poseSave(self):
        asset_name = self.UI.asset_comboBox.currentText()
        pose_name = self.UI.posename_lineEdit.text()
        imagepath = fnc.poseEntry(asset_name, pose_name)
        self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon(imagepath),pose_name))

    def assetDelete(self):
        print "delete"

    def poseLoad(self):
        asset_name = self.UI.load_comboBox.currentText()
        currentitem = self.UI.pose_listWidget.currentItem()
        pose_name = currentitem.text()
        fnc.readPose(asset_name, pose_name)
