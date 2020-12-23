# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:02:11 2020

@author: the one and only, the almighty, the all-knowig, the man the myth the legend.
"""
import sys, os
import webbrowser
import subprocess
from subprocess import Popen, PIPE

#from PyQt5 import QtCore, QtWidgets, uic
import PySide2
from PySide2 import QtCore, QtWidgets
from PySide2.scripts.pyside_tool import qt_tool_wrapper
from PySide2.QtWidgets import QMainWindow
from LibraryViewer import LibraryViewer
from SchematicViewer import SchematicViewer

Spyce_version = '1.0'

# =============================================================================
# compile resource file
# =============================================================================
def QtCompile(qt_tool, src, dest):
    p = os.path.dirname(__file__)
    
    src = os.path.join(p, "QtDesignerFiles", src)
    dest = os.path.join(p, dest)
    
    if not os.path.exists(dest) or \
              os.path.getmtime(src) >  os.path.getmtime(dest):
        print('compiling file {}'.format(src))
    
        #    from PyQt5 import pyrcc_main
        #    
        #    print('compiling resources file')
        #    pyrcc_main.processResourceFile([QtResource_file], PyResource_file, listFiles=False)
        pyside_dir = os.path.dirname(PySide2.__file__)
        exe = os.path.join(pyside_dir, qt_tool)
    
        cmd = [exe] + ['-g', 'python', '-o', dest, src]
        proc = Popen(cmd, stderr=PIPE)
        out, err = proc.communicate()
        if err:
            msg = err.decode("utf-8")
            print("Error: {}\nwhile executing '{}'".format(msg, ' '.join(cmd)))
            sys.exit()


QtCompile("rcc", "Spyce.qrc", 'Spyce_rc.py')
QtCompile("uic", "Spyce_main.ui", 'Spyce_ui.py')
    
from Spyce_ui import Ui_MainWindow

# =============================================================================
# compile uic file    
# =============================================================================


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
        # self.actionInput_Port.triggered.connect(      self.SchematicViewer.addInPort)
        # self.actionOutput_Port.triggered.connect(     self.SchematicViewer.addOutPort)
        # self.actionNode.triggered.connect(            self.SchematicViewer.addNode)
        # self.actionConnection.triggered.connect(      self.SchematicViewer.addConnection)
        # self.actionText.triggered.connect(            self.SchematicViewer.addText)
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
 
            
    def GetLanguage(self):
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
