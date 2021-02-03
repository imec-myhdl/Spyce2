#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Connection Class
"""
from Qt import QtWidgets, QtGui, QtCore # see https://github.com/mottosso/Qt.py
from preferences import colors, LW
#from   SpyceCommon import gridPos


class Vertex(QtWidgets.QGraphicsPathItem):
    """Vertex of Connection"""
    def __init__(self, parent, pos):
        super(Vertex, self).__init__(parent)
        self.parent = parent
        self.setPos(pos)
        self.setFlag(self.ItemSendsGeometryChanges, True)
        self.pos0 = QtCore.QPointF()
        self.setPen(parent.pen())
        
        self.shapeDeselected = QtGui.QPainterPath()
        self.shapeDeselected.addRect(-1e-6,-1e-6, 2e-6, 2e-6) # basically a dot

        self.shapeSelected = QtGui.QPainterPath()
        self.shapeSelected.addRect(-LW,-LW,LW*2,LW*2) # wider rect

        self.setPath(self.shapeDeselected)

        
    def remove(self):
        return self.parent.rm_vertex(self)
                
    def itemChange(self, change, value):
        if change == self.ItemSelectedHasChanged:
            if value: #selection starts
                self.pos0 = self.pos()
                self.setPath(self.shapeSelected)
            else: # selection ends
                self.setPath(self.shapeDeselected)
        elif change == self.ItemPositionChange:
            #restrict movement to horizontal or vertical            
            if abs(value.x()-self.pos0.x()) > abs(value.y()-self.pos0.y()): # 'horizontal':
                return QtCore.QPointF(value.x(), self.pos0.y())
            else:
                return QtCore.QPointF(self.pos0.x(), value.y())
        elif change == self.ItemPositionHasChanged:
            self.parentItem().update_path() #update drawing if the vertices have moved
        else:
            return super().itemChange(change, value)
        

class Connection(QtWidgets.QGraphicsPathItem):
    """Connects one port to another."""

    def __init__(self, pos):
        super(Connection, self).__init__()
        self.lineColor = colors['connection']
        self.LW = LW
        pen = QtGui.QPen(self.lineColor)
        pen.setWidth(self.LW)
        self.setPen(pen)
        self.vertices = [Vertex(self, pos)]

    def add_vertex(self, pos):
        for p in self.xy(pos):
            v = Vertex(self, p)
            self.vertices.append(v)
        self.update_path()
            
    def update_path(self, pos=None):
        p = QtGui.QPainterPath()
        p.moveTo(self.vertices[0].pos())
        for v in self.vertices[1:]:
            p.lineTo(v.pos())
        for pt in self.xy(pos):
            p.lineTo(pt)
        self.setPath(p)
            
    
    def rm_vertex(self, item=None):
        '''returns True if connection was deleted (0 vertices left)'''
        if len(self.vertices) >= 1:
            ix = self.vertices.index(item) if item else -1 # last one
            v = self.vertices.pop(ix)
            self.scene().removeItem(v)
        if item and len(self.vertices) == 1: # item is only set when deleting selected vertices via Vertex.remove()
            v = self.vertices.pop()
            self.scene().removeItem(v)
        if len(self.vertices) == 0:
            self.scene().removeItem(self)
            return True
        # redraw
        self.update_path()
        return False
        
    def finish(self, pos=None):
        if pos:
            self.add_vertex(pos)
        self.setMutable(True)
        
        
    def xy(self, pos):
        '''returns point[s] to come from p0 to p1 in an othogonal fashion'''
        if pos is None:
            return []
        p0 = self.vertices[-1].pos()
        dx = pos.x() - p0.x()
        dy = pos.y() - p0.y()
        if dx == 0 or dy == 0:
            return [pos]
        if abs(dx) > abs(dy):
            pt = QtCore.QPointF(pos.x(),p0.y())
        else:
            pt = QtCore.QPointF(p0.x(),pos.y())
        return [pt, pos]


    def setMutable(self, mutable=False):
        for i in self.vertices:
            i.setFlag(i.ItemIsMovable, mutable)
            i.setFlag(i.ItemIsSelectable, mutable)
