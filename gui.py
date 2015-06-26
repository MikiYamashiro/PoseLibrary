# -*- coding: utf-8 -*-

import os
import sys
from PySide import QtCore, QtGui
from PySide.QtUiTools import QUiLoader

from maya import OpenMayaUI
import shiboken

sys.path.append('/Users/yamashiromiki/Documents/Data/PoseLibrary/code')
import function as fnc
reload(fnc)

def getMayaMainWindow():
    maya_ptr = OpenMayaUI.MQtUtil_mainWindow()
    return shiboken.wrapInstance(maya_ptr, QtGui.QMainWindow)

class GUI(QtGui.QMainWindow):
 
    def __init__(self, parent=None):
        super(GUI, self).__init__(getMayaMainWindow())
        loader = QUiLoader()
        uiFilePath = os.path.join('/Users/yamashiromiki/Documents', 'PoseLibrary.ui')
        self.UI = loader.load(uiFilePath)
        self.setCentralWidget(self.UI)
        self.setWindowTitle('PoseLibrary')
        self.resize(510, 750)
        
        self.__setui()
        self.__setSlots()


    def __setui(self):
        assetlist=fnc.searchAssetName()
        for asset in assetlist:
            if os.path.isdir:
                if not asset == ".DS_Store":
                    self.UI.asset_comboBox.addItem(asset)
                    self.UI.load_comboBox.addItem(asset)

        asset_name = self.UI.load_comboBox.currentText()
        posedict = fnc.searchPoseList(asset_name)
        #self.UI.pose_listWidget.setModel(myListModel)
        self.UI.pose_listWidget.setViewMode(QtGui.QListView.IconMode)
        self.UI.pose_listWidget.setIconSize(QSize(200,200))

        for k,v in posedict.items():
            self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon(v),str(k)))
        #self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon("/Users/yamashiromiki/Documents/Data/PoseLibrary/image/SolKing/run.png"),"Earth"))


    def __setSlots(self):
        
        self.UI.entry_pushButton.clicked.connect(self.assetEntryWindow)
        self.UI.save_pushButton.clicked.connect(self.poseSave)
        self.UI.delete_pushButton.clicked.connect(self.assetDelete)

        self.UI.load_pushButton.clicked.connect(self.poseLoad)

        self.UI.load_comboBox.currentIndexChanged.connect(self.loadName)

    def loadName(self):
        self.UI.pose_listWidget.clear()
        asset_name = self.UI.load_comboBox.currentText()
        posedict = fnc.searchPoseList(asset_name)

        for k,v in posedict.items():
            self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon(v),str(k)))

    def assetEntryWindow(self):
        print "asset entry"
        print self.UI.asset_lineEdit.text()
        asset_name = self.UI.asset_lineEdit.text()
        fnc.assetSetUp(asset_name)
        # Add Items ComboBox
        self.UI.asset_comboBox.addItem(asset_name)
        self.UI.load_comboBox.addItem(asset_name)

    def poseSave(self):
        print self.UI.asset_comboBox.currentText()
        print self.UI.posename_lineEdit.text()
        asset_name = self.UI.asset_comboBox.currentText()
        pose_name = self.UI.posename_lineEdit.text()
        imagepath = fnc.poseEntry(asset_name, pose_name)

        self.UI.pose_listWidget.addItem(QtGui.QListWidgetItem(QtGui.QIcon(imagepath),pose_name))

    def assetDelete(self):
        print "delete"


    def poseLoad(self):
        print "test"
        asset_name = self.UI.load_comboBox.currentText()
        currentitem = self.UI.pose_listWidget.currentItem()
        pose_name = currentitem.text()
        print asset_name
        print pose_name
        fnc.readPose(asset_name, pose_name)
         

def main():
    ui = GUI()
    ui.show()


main()

