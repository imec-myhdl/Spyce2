#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:11:43 2020

@author: jonathan
"""
from PySide2 import QtCore, QtWidgets

class LibraryViewer(object):
    def __init__(self, gui_top):
        self.tabs = gui_top.LibrarySymbolView
        self.tree = gui_top.LibraryTreeView
        
        # add Quicksel tab
        self.quickSelTab = QtWidgets.QComboBox()        
        self.tabs.setCornerWidget(self.quickSelTab, QtCore.Qt.TopLeftCorner)
        
        # actions
        self.tabs.currentChanged.connect(self.setCurrentTab)
        self.quickSelTab.currentIndexChanged.connect(self.setCurrentTab)
        
        # init
        self.updateQuickSelTab()
        self.ToggleView()
        
    def updateQuickSelTab(self):
        libnames = []
        for i in range(self.tabs.count()): # iterate over tabs
            libnames.append(self.tabs.tabText(i))
        self.quickSelTab.addItems(libnames)

    def setCurrentTab(self, ix):
        self.tabs.setCurrentIndex(ix)
        self.quickSelTab.setCurrentIndex(ix)
        
    # =========================================================================
    # actions
    # =========================================================================
    def ToggleView(self):
        '''toggle viewing mode (symbol/tree)'''
        if self.tabs.isVisible():
            self.tabs.hide()
            self.tree.show()
        else:
            self.tabs.show()
            self.tree.hide()
            
    def New(self):
        pass #TODO
    
    def ImportFromFile(self):
        pass #TODO