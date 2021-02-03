#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:17:38 2020

@author: jonathan
"""

from Qt import QtCore, QtGui, QtWidgets # see https://github.com/mottosso/Qt.py
from Qt.QtWidgets import QGraphicsScene, QGraphicsView
from .SpyceCommon import gridPos
from .Connection import Connection, Vertex


class Editor(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = EditorScene(self)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        self.setAcceptDrops(True)
        self.normalCursor     = self.cursor()
        self.inPortCursor     = QtGui.QCursor(QtGui.QPixmap(u":/icons/Spyce_Icons/inport.svg"))
        self.outPortCursor    = QtGui.QCursor(QtGui.QPixmap(u":/icons/Spyce_Icons/outport.svg"))
        self.connectionCursor = QtGui.QCursor(QtGui.QPixmap(u":/icons/Spyce_Icons/node.svg"))
        self.textCursor       = QtGui.QCursor(QtGui.QPixmap(u":/icons/feather/type.svg"))
        self.currentscale = 1.0
        self.mode = 'normal'

    def wheelEvent(self, event):
        factor = 1.41 ** (event.angleDelta().y()/ 240.0)
        self.currentscale *= factor
        # zoom around mouse position, not the anchorNoneNone
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        pos = self.mapToScene(event.pos())
        self.scale(factor, factor)
        delta =  self.mapToScene(event.pos()) - pos
        self.translate(delta.x(), delta.y())

    def setMode(self, mode):
        if mode == 'inPort':
            self.setCursor(self.inPortCursor)
        elif mode == 'outPort':
            self.setCursor(self.outPortCursor)
        elif mode == 'connection':
            self.setCursor(self.connectionCursor)
        elif mode == 'text':
            self.setCursor(self.textCursor)
        else:
            mode = 'normal'
            self.setCursor(self.normalCursor)
            self.scene.escapeConnection() #To prevent unfinished connections when switching
        self.mode = mode

class EditorScene(QGraphicsScene):
    def __init__(self, view):
        super().__init__()
        self.setSceneRect(QtCore.QRectF(-2000, -2000, 4000, 4000))
        self.item = None # current item
        self.view = view
        self.view.setScene(self)
        self.installEventFilter(self)
#        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.view)
        self.view.show()
            
    def connectionStartOrExtend(self, event):
        pos = gridPos(event.scenePos())

        if isinstance(self.item, Connection):
            self.item.add_vertex(pos)
        else:
            self.item = Connection(pos)
            self.addItem(self.item)
            # enable dynamic update
            self.view.setMouseTracking(True)

    def connectionFinish(self, event):
        pos = gridPos(event.scenePos())
        if isinstance(self.item, Connection):
            self.item.finish(pos)
        self.item = None
        # end dynamic update
        self.view.setMouseTracking(False)
        
    def connectionMove(self, event):
        self.mousePos = gridPos(event.scenePos())
        if isinstance(self.item, Connection):
            self.item.update_path(self.mousePos)
    
    def escapeConnection(self):
        if isinstance(self.item, Connection):
            self.removeItem(self.item)
            self.item = None


    def eventFilter(self, obj, event): 
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_0:
                print('Selected', self.selectedItems())
            if event.key() == QtCore.Qt.Key_9:
                for i in self.items():
                    if isinstance(i, Vertex):
                        if i.isSelected():
                            print('Selected', i)
        if self.view.mode == 'connection':
            # mouse left-click: start a connection, or add a vertex
            # mouse right-click: finish connection
            # key escape: kill current connection, switch to normal mode
            # key backsapce: remove last vertex
            if event.type() ==  QtCore.QEvent.GraphicsSceneMouseMove:
                 self.connectionMove(event)                 
            elif event.type() ==  QtCore.QEvent.GraphicsSceneMousePress:
                if event.button() == QtCore.Qt.LeftButton:
                    self.connectionStartOrExtend(event)
                elif event.button() == QtCore.Qt.RightButton:
                    self.connectionFinish(event)                
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Backspace:
                    if isinstance(self.item, Connection):
                        if self.item.rm_vertex(): # remove alltogether if this was last vertex
                            self.item = None
                        else:
                            self.item.update_path(self.mousePos)

        elif self.view.mode == 'normal':
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() in [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete]:
                    for item in self.selectedItems():
                        if isinstance(item, Vertex):
                            item.remove() 

        return super().eventFilter(obj, event)


class SchematicViewer(object):
    def __init__(self, gui_top):
        self.tabWidget = gui_top.tabWidget
        self.tabWidget.clear()
        del gui_top.Untitled #Remove from namespace, was created with QtDesigner
        
        self.New()
        self.mode = 'normal'
        #Signals
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        
    def New(self):
        name="Untitled"       
        new_tab = Editor()
        used_names = [self.tabWidget.tabText(ix) for ix in range(self.tabWidget.count())]

        i = 1
        tabname = name
        while tabname in used_names:
            tabname = '{}_{}'.format(name, i)
            i += 1
            
        self.tabWidget.addTab(new_tab, tabname)
        
    def closeTab(self, ix):
        self.tabWidget.removeTab(ix)
        
    def inPortMode(self):
        self.setMode('inPort')
    
    def outPortMode(self):
        self.setMode('outPort')
    
    def connectionMode(self):
        self.setMode('connection')
    
    def normalMode(self):
        self.setMode('normal')
    
    def textMode(self):
        self.setMode('text')
    
    def setMode(self, mode):
        self.tabWidget.currentWidget().setMode(mode)
        
