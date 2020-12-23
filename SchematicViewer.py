#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:17:38 2020

@author: jonathan
"""

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QGraphicsScene, QGraphicsView

class SchematicViewer(object):
    def __init__(self, gui_top):
        self.tabWidget = gui_top.tabWidget
        
        self.tabWidget.clear()
        del gui_top.Untitled #Remove from namespace, was created with QtDesigner
        
        self.New()
        
        #Signals
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        
    def New(self):
        name="Untitled"
        
        scene = QGraphicsScene()
        new_view = QGraphicsView(scene)
        
        used_names = [self.tabWidget.tabText(ix) for ix in range(self.tabWidget.count())]
                
        i = 1
        tabname = name
        while tabname in used_names:
            tabname = '{}_{}'.format(name, i)
            i += 1
            
        self.tabWidget.addTab(new_view, tabname)
        new_view.show()
        
    def closeTab(self, ix):
        self.tabWidget.removeTab(ix)