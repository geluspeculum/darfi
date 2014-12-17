#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is a part of DARFI project (dna Damage And Repair Foci Imager)
#    Copyright (C) 2014  Ivan V. Ozerov, Grigoriy A. Armeev
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as·
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License v2 for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys,os,functools, pickle
sys.path.append(os.path.join('..','engine'))
import pic_an
import folder_widget
import settings_window
from settings import Settings
from PyQt4 import QtGui, QtCore


#### Uncomment these lines if building py2exe binary with window output only
## import warnings
## warnings.simplefilter('ignore')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

          
    
class DarfiUI(QtGui.QMainWindow):
    
    def __init__(self):
        super(DarfiUI, self).__init__()
        self.settings=Settings()
        self.workDir=unicode(QtCore.QDir.currentPath())
        self.showMiniatures=True
        self.oldDirsWithImages=[]
        self.oldFoci_rescale_min = None
        self.oldFoci_rescale_max = None
        self.lastCalc=False
        self.settingsChanged=True
        self.initUI()
        if os.path.isfile(os.path.join(unicode(QtCore.QDir.currentPath()),"Darfi_session.dcf")):
            self.readSettings(os.path.join(unicode(QtCore.QDir.currentPath()),"Darfi_session.dcf"))

    
    def loadDefaultSettings(self):
        self.settings=Settings()
        self.workDir=unicode(QtCore.QDir.currentPath())
        self.fociNameField.setText(self.settings.foci_name)
        self.nuclNameField.setText(self.settings.nuclei_name)
        self.outfileField.setText(self.settings.outfile)
        self.fileMenuArea.setWorkDir(self.workDir)
        print "Default settings loaded"
        #self.fileMenuArea.updateWorkDir()
            
    
    def dumpSettings(self,filename=None):
        if not(filename):
            filename=unicode(QtGui.QFileDialog.getSaveFileName(self,'Write DARFI config file', '','DARFI Config File, *.dcf;;All Files (*)'))
        if filename != "":
            #that is rude but it works (
            if filename[-4:] != '.dcf':
                filename+=unicode('.dcf')
            with open(filename, 'w+') as f:
                pickle.dump([self.fileMenuArea.workDir,self.settings,self.fileMenuArea.getCheckedPaths()], f)

    def readSettings(self,filename=None):
        if not(filename):
            filename=unicode(QtGui.QFileDialog.getOpenFileName(self,'Open DARFI config file', '','DARFI Config File, *.dcf;;All Files (*)'))
        if filename != "":
            with open(filename) as f:
                print "Loading previous config"
                self.workDir,self.settings, paths = pickle.load(f)
                self.fociNameField.setText(self.settings.foci_name)
                self.nuclNameField.setText(self.settings.nuclei_name)
                self.outfileField.setText(self.settings.outfile)
                self.fileMenuArea.openWorkDir(self.workDir)
                self.fileMenuArea.setCheckedFromPaths(paths)
                
                
    def openSettings(self):
        self.settingsWindow = settings_window.SettingsWindow(self.settings)
        self.settingsWindow.exec_()
        self.settings,self.settingsChanged = self.settingsWindow.getSettings()

    def closeEvent(self, event):
        print "Closing DARFI, goodbye"
        filename=os.path.join(unicode(QtCore.QDir.currentPath()),"Darfi_session.dcf")
        self.dumpSettings(filename)          
            
        
    def resizeEvent( self, oldsize):
        ''' override resize event to redraw pictures'''
        self.updateImages()
    
        
    def setNuclei_name(self,text):
        self.settings.nuclei_name = unicode(text)
        
    def setFoci_name(self,text):
        self.settings.foci_name = unicode(text)
        
    def setOutfile(self,text):
        self.settings.outfile = unicode(text)
#            
#    def selectWorkDir(self):
#        self.model.unCheckAll()
#        
#        #self.workDir=
#        tempDir=QtGui.QFileDialog.getExistingDirectory(directory=self.workDir)
#        print type(tempDir)
#        if tempDir != "":
#            self.workDir=tempDir
#            self.fileMenu.setRootIndex(self.model.index(self.workDir))
#   
#    def selectFileName(self):
#        filename=QtGui.QFileDialog.getSaveFileName()
#        print filename
        
    def reUpdateImages(self):
        self.showMiniatures=True
        self.updateImages()
        
    def reUpdateImage(self):
        self.showMiniatures=False
        self.updateImages()
        
    def updateImages(self):
        if self.showMiniatures:
            try:
                self.lbl1.clear()
                
                imageDir = self.fileMenuArea.selectedImageDir
                if imageDir=="":
                    self.lbl1.clear()
                    self.lbl2.clear()
                    self.lbl3.clear()
                    self.lbl4.clear()
                    self.lbl5.clear()
                    self.lbl6.clear()
                else:
                    path = imageDir.absolutePath()
                    filters = ["*.TIF", "*.tif"]

                    imageDir.setNameFilters(filters)
                    
                    #FIXME use margins e.t.c
                    sizex=self.imagePreviewArea.width()/2-10
                    sizey=self.imagePreviewArea.height()/3-10
                    try:
                        imageName1 = imageDir.entryList()[0]

                        pix1 = QtGui.QPixmap(path + QtCore.QDir.separator() + imageName1)
                        self.lbl1.resize(sizex,sizey)
                        self.lbl1.setPixmap(pix1.scaled(self.lbl1.size(), QtCore.Qt.KeepAspectRatio))
                        self.lbl1.update()

                    except IndexError:
                        self.lbl1.clear()
         
                    try:
                        imageName2 = imageDir.entryList()[1]
                        pix2 = QtGui.QPixmap(path + QtCore.QDir.separator() + imageName2)
                        self.lbl2.resize(sizex,sizey)

                        self.lbl2.setPixmap(pix2.scaled(self.lbl2.size(), QtCore.Qt.KeepAspectRatio))
                        self.lbl2.update()
                    except IndexError:
                        self.lbl2.clear()
                        
                    filters = ["*.jpg", "*.JPG"]
                    imageDir.setNameFilters(filters)
                    try:
                        pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[0])
                        self.lbl3.resize(sizex,sizey)
                        self.lbl3.update()
                        self.lbl3.setPixmap(pix.scaled(self.lbl3.size(), QtCore.Qt.KeepAspectRatio))
                        self.lbl3.update()
                    except IndexError:
                        self.lbl3.clear()
                    
                    try:    
                        pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[1])
                        self.lbl4.resize(sizex,sizey)
                        self.lbl4.setPixmap(pix.scaled(self.lbl4.size(), QtCore.Qt.KeepAspectRatio))
                        self.lbl4.update()
                    except IndexError:
                        self.lbl4.clear()
                    
                    try:    
                        pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[2])
                        self.lbl5.resize(sizex,sizey)
                        self.lbl5.setPixmap(pix.scaled(self.lbl5.size(), QtCore.Qt.KeepAspectRatio))
                        self.lbl5.update()
                    except IndexError:
                        self.lbl5.clear()
                    
                    try:    
                        pix = QtGui.QPixmap(path + QtCore.QDir.separator() + imageDir.entryList()[3])
                        self.lbl6.resize(sizex,sizey)
                        self.lbl6.setPixmap(pix.scaled(self.lbl6.size(), QtCore.Qt.KeepAspectRatio))
                        self.lbl6.update()
                    except IndexError:
                        self.lbl6.clear()
            except AttributeError:
                ()
        else:
            imageName = self.fileMenuArea.selectedImage
            pix1 = QtGui.QPixmap(imageName)
            self.lbl2.clear()
            self.lbl2.resize(0,0)
            self.lbl3.clear()
            self.lbl3.resize(0,0)
            self.lbl4.clear()
            self.lbl4.resize(0,0)
            self.lbl5.clear()
            self.lbl5.resize(0,0)
            self.lbl6.clear()
            self.lbl6.resize(0,0)
            sizex=self.imagePreviewArea.width()-30
            sizey=self.imagePreviewArea.height()-60
            self.lbl1.resize(sizex,sizey)
            self.lbl1.setPixmap(pix1.scaled(self.lbl1.size(), QtCore.Qt.KeepAspectRatio))
            self.lbl1.update()
           
       
    def initUI(self):
              

################## FILEMENU AREA  ########################################

        self.fileMenuArea = folder_widget.FolderWidget(self)
        self.fileMenuArea.signal_update_images.connect(self.reUpdateImages)
        self.fileMenuArea.signal_update_image.connect(self.reUpdateImage)
        
################## IMAGE AREA  ########################################

        self.imagePreviewArea = QtGui.QScrollArea(self)
        
        self.imagePreviewLayout = QtGui.QGridLayout(self.imagePreviewArea)
        self.connect(self.imagePreviewArea, QtCore.SIGNAL("resizeEvent()"), self.updateImages)
        self.lbl1 = QtGui.QLabel(self)
        self.imagePreviewLayout.addWidget(self.lbl1, 0,0)
        self.lbl2 = QtGui.QLabel(self)
        self.imagePreviewLayout.addWidget(self.lbl2, 0,1)
        self.lbl3 = QtGui.QLabel(self)
        self.imagePreviewLayout.addWidget(self.lbl3, 1,0)
        self.lbl4 = QtGui.QLabel(self)
        self.imagePreviewLayout.addWidget(self.lbl4, 1,1)
        self.lbl5 = QtGui.QLabel(self)
        self.imagePreviewLayout.addWidget(self.lbl5, 2,0)
        self.lbl6 = QtGui.QLabel(self)
        self.imagePreviewLayout.addWidget(self.lbl6, 2,1)
       
################## SETTINGS AREA  ########################################

        buttonArea = QtGui.QWidget(self)
        buttonLayout = QtGui.QVBoxLayout(buttonArea)
        
        self.openSettingsButton = QtGui.QPushButton("Settings")
        self.openSettingsButton.clicked.connect(self.openSettings)
        buttonLayout.addWidget(self.openSettingsButton)
        self.pbar = QtGui.QProgressBar(self)

        nuclNameFieldLabel = QtGui.QLabel(self)
        nuclNameFieldLabel.setText("Files with nuclei:")
        self.nuclNameField = QtGui.QLineEdit()
        self.nuclNameField.setText(self.settings.nuclei_name)
        self.nuclNameField.textChanged[str].connect(lambda: self.setNuclei_name(self.nuclNameField.displayText()))
        buttonLayout.addWidget(nuclNameFieldLabel)
        buttonLayout.addWidget(self.nuclNameField)
        
        fociNameFieldLabel = QtGui.QLabel(self)
        fociNameFieldLabel.setText("Files with foci:")
        self.fociNameField = QtGui.QLineEdit()
        self.fociNameField.setText(self.settings.foci_name)
        self.fociNameField.textChanged[str].connect(lambda: self.setFoci_name(self.fociNameField.displayText()))
        buttonLayout.addWidget(fociNameFieldLabel)
        buttonLayout.addWidget(self.fociNameField)
        
        outfileFieldLabel = QtGui.QLabel(self)
        outfileFieldLabel.setText("Outfile name:")
        self.outfileField = QtGui.QLineEdit()
        self.outfileField.setText(self.settings.outfile)
        self.outfileField.textChanged[str].connect(lambda: self.setOutfile(self.outfileField.displayText()))
        buttonLayout.addWidget(outfileFieldLabel)
        buttonLayout.addWidget(self.outfileField)
        
        rescaleButton = QtGui.QPushButton("Get scale from selection")
        rescaleButton.clicked.connect(self.fileMenuArea.getScaleFromSelected)
        buttonLayout.addWidget(rescaleButton)
        
        runCalcButton = QtGui.QPushButton("Calculate")
        runCalcButton.clicked.connect(self.fileMenuArea.calculateSelected)
        runCalcButton.setMinimumHeight(40)
        buttonLayout.addWidget(runCalcButton)
        

        
        self.pbar.hide()
        buttonLayout.addWidget(self.pbar)
       
        spacer=QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding) 
        buttonLayout.addSpacerItem(spacer)
        
        nuclLogLabel = QtGui.QLabel(self)
        nuclLogLabel.setText("Log:")
        buttonLayout.addWidget(nuclLogLabel)        
                
        self.logText = QtGui.QTextEdit()
        self.logText.setMaximumHeight(100)
        self.logText.setReadOnly(True)
        self.logText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logText.append("Welcome to DARFI! ")
        self.logger = Logger(self.logText)
        #self.errors = Logger(self.logText)
        sys.stdout = self.logger
        #sys.stderr = self.errors
        buttonLayout.addWidget(self.logText)

        buttonLayout.setAlignment(QtCore.Qt.AlignTop)
        
################## STATUS AREA  ########################################

        self.statusArea = QtGui.QTableWidget(self)
        self.statusArea.setRowCount(2)
        self.statusArea.setColumnCount(8)
        self.statusArea.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Cell number"))
        self.statusArea.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Cell area"))
        self.statusArea.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Mean intensity"))
        self.statusArea.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("Rel foci number"))
        self.statusArea.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("Foci area"))
        self.statusArea.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem("Foci intensity"))
        self.statusArea.setHorizontalHeaderItem(6, QtGui.QTableWidgetItem("Foci soid"))
        self.statusArea.setHorizontalHeaderItem(7, QtGui.QTableWidgetItem("Foci size"))
        self.statusArea.setVerticalHeaderItem(0, QtGui.QTableWidgetItem("Mean"))
        self.statusArea.setVerticalHeaderItem(1, QtGui.QTableWidgetItem("MSE"))
        
     
        

        

################## COMPOSITING  ########################################



        windowInitWidth = 1024
        windowInitHeight = 768


        icon = QtGui.QIcon()
        
        homepath = os.path.abspath(os.path.dirname(os.getcwd()))
        iconpath = os.path.join(homepath, 'misc', 'darfi.ico')

        if os.path.isfile(iconpath):
            icon.addPixmap(QtGui.QPixmap(_fromUtf8(iconpath)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(_fromUtf8(os.path.join(os.getcwd(), 'misc', 'darfi.ico'))), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        hbox = QtGui.QHBoxLayout()

        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.imagePreviewArea)
        splitter1.addWidget(buttonArea)
        splitter1.setSizes([windowInitWidth-400,200])
        splitter1.splitterMoved.connect(self.updateImages)
        

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.statusArea)
        splitter2.setSizes([windowInitHeight-200,windowInitHeight/200])
        splitter2.splitterMoved.connect(self.updateImages)
        
        splitter3 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter3.addWidget(self.fileMenuArea)
        splitter3.addWidget(splitter2)
        splitter3.setSizes([200,windowInitWidth-200])
        splitter3.splitterMoved.connect(self.updateImages)

        hbox.addWidget(splitter3)

        hboxWidget=QtGui.QWidget(self)
        hboxWidget.setLayout(hbox)
        self.setCentralWidget(hboxWidget)
       
        self.setGeometry(0, 0,windowInitWidth, windowInitHeight)
        self.setWindowTitle('DARFI')
        self.setWindowIcon(icon)
        self.createActions()
        self.createMenus()
        self.show()
        
    ################## MAIN MENU AREA  ########################################

    def createActions(self):
        self.settingsAct = QtGui.QAction("&Settings...", self, shortcut="Ctrl+S",triggered=self.openSettings)
        
        self.settingsDefAct = QtGui.QAction("&Load Defaults...", self, shortcut="Ctrl+D",triggered=self.loadDefaultSettings)

        self.openSettingsAct = QtGui.QAction("&Load settings...", self, shortcut="Ctrl+R",triggered=self.readSettings)
                
        self.saveSettingsAct = QtGui.QAction("&Write settings...", self, shortcut="Ctrl+W",triggered=self.dumpSettings)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.settingsAct)
        self.fileMenu.addAction(self.settingsDefAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openSettingsAct)
        self.fileMenu.addAction(self.saveSettingsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = QtGui.QMenu("&About", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.helpMenu)

    def about(self):
        QtGui.QMessageBox.about(self, "About DARFI",
                "<p><b>DARFI</b> is short of dna Damage And Repair Foci Imager <br>"
                "Copyright (C) 2014  Ivan V. Ozerov<br>"
                "This program is free software; you can redistribute it and/or modify "
                "it under the terms of the GNU General Public License version 2 as "
                "published by the Free Software Foundation.</p>")


         

class Logger(object):
    def __init__(self, output):
        self.output = output
 
    def write(self, string):
        if not (string == "\n"):
            trstring = QtGui.QApplication.translate("MainWindow", string.strip(), None, QtGui.QApplication.UnicodeUTF8)
            self.output.append(trstring)

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = DarfiUI()
    ex.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
