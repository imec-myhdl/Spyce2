# -*- coding: utf-8 -*-
"""
Simple Python Circuit Editor
Spyce Main routine
"""
version_info = (1, 0, 0) # Spyce_version = '1.0.0'
version = '.'.join(str(c) for c in version_info)

# This module also checks for pre-loaded Qt environments
from SpyceLib.misc import QtCompile

import sys

import webbrowser
Spyce_version = '1.0'


# see https://github.com/mottosso/Qt.py
from Qt import QtCore, QtWidgets
from Qt.QtWidgets import QMainWindow

from SpyceLib.LibraryViewer import LibraryViewer
from SpyceLib.SchematicViewer import SchematicViewer

# =============================================================================
# compile uic/qrc files and import Ui
# =============================================================================
QtCompile("Spyce.qrc", 'Spyce_rc.py')
QtCompile("Spyce_main.ui", 'Ui/Spyce_ui.py')

from Ui.Spyce_ui import Ui_MainWindow

class gui_top(QMainWindow, Ui_MainWindow):
    #--------------------------------------------------------------------------
    def __init__(self):
        """
        This is the constructor of the 'gui_top' class. This function will be executed
        when the class is used. This function initializes the default tabs (console, register),
        menus (File, Port) and the items related to that. Custom operations may be added to init_tabs
        """

        #Initialize GUI
        super().__init__()
        self.setupUi(self)
        
        self.LibraryViewer = LibraryViewer(self)
        
        self.SchematicViewer = SchematicViewer(self)
        
        # =====================================================================
        # connect  actions
        # =====================================================================
        self.actionQuit.triggered.connect(QtWidgets.QApplication.instance().quit)

        # SchematicViewer actions
        self.actionNew.triggered.connect(             self.SchematicViewer.New)
        # self.actionOpen.triggered.connect(            self.SchematicViewer.Open)
        # self.actionSave.triggered.connect(            self.SchematicViewer.Save)
        # self.actionSave_as.triggered.connect(         self.SchematicViewer.SaveAs)
        # self.actionPrint.triggered.connect(           self.SchematicViewer.Print)
        # self.actionPrint_hierarchy.triggered.connect( self.SchematicViewer.PrintHierarchy)
        self.actionInput_Port.triggered.connect(      self.SchematicViewer.inPortMode)
        self.actionOutput_Port.triggered.connect(     self.SchematicViewer.outPortMode)
        self.actionConnection.triggered.connect(      self.SchematicViewer.connectionMode)
        self.actionNormal.triggered.connect(          self.SchematicViewer.normalMode)
        self.actionText.triggered.connect(            self.SchematicViewer.textMode)
        # self.actionCut.triggered.connect(             self.SchematicViewer.Cut)
        # self.actionCopy.triggered.connect(            self.SchematicViewer.Copy)
        # self.actionPaste.triggered.connect(           self.SchematicViewer.Paste)
        # self.actionProperties.triggered.connect(      self.SchematicViewer.Properties)
        # Simulation actions
        # self.actionNetlist.triggered.connect(         self.Simulation.Netlist)
        # self.actionNetlist_and_Run.triggered.connect (self.Simulation.NetlistAndRun)

        # help
        self.actionManual.triggered.connect(          self.Manual)
        self.actionWebsite.triggered.connect(         self.Website)
        self.actionabout.triggered.connect(           self.About)

        # Library actions
        self.actionNew_Library.triggered.connect(     self.LibraryViewer.New)
        self.actionimport_from_file.triggered.connect(self.LibraryViewer.ImportFromFile)
        self.actiontoggle_layout.triggered.connect(   self.LibraryViewer.ToggleView)

        # =====================================================================
        # create menuLanguage entries
        # =====================================================================
        self.languageActionGroup = QtWidgets.QActionGroup(self)
        self.languageActionGroup.setExclusive(True)
        for lang in 'MyHdl SystemVerilog Xyce'.split():
            va = self.menuLanguage.addAction(lang)
            va.setCheckable(True)
            va.setActionGroup(self.languageActionGroup)
            va.setData(lang)

        # select first entry
        self.languageActionGroup.actions()[0].setChecked(True)
 
            
    def GetNetlistLanguage(self):
        for va in self.languageActionGroup.actions():
            if va.isChecked():
                return va.data()
        
    def Website(self):
        url = r'https://github.com/imec-myhdl/Spyce'
        webbrowser.open(url, new=1, autoraise=True)

    def Manual(self):
        pass # TODO

    def About(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Spyce:\nSimple python circuit editor\nVersion {}".format(Spyce_version))
        msgBox.exec_();


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)

    window = gui_top()
    window.show()
    sys.exit(app.exec_())
