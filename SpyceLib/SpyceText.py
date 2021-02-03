# -*- coding: utf-8 -*-
"""
TextItem Class
"""

# Standard library imports
from collections import OrderedDict

# Third party imports
from  Qt import QtGui, QtWidgets, QtCore # see https://github.com/mottosso/Qt.py

# Local application imports
from preferences import colors, stdfont

class textItem(QtWidgets.QGraphicsTextItem):
    '''convenience class, extension of QGraphicsSimpleTextItem, that realises aligned text
    textItem.setFlipped() will mirror the text  (in place)
    textItem.setNormal() will put txt in normal (non-mirrored) state
    
    anchor is (look at numpad):
    1: bottom-left
    2: bottom-center
    3: bottom-right
    4: center-left
    5: center-center
    6: center-right
    7: top-left
    8: top-center
    9: top-right'''
    def __init__(self, text, anchor=1, parent=None):
        super().__init__(str(text), parent)
        self.anchor = anchor
        self.scale = 1
        # compute dx, dy absed on anchor
        self.setAnchor()
        self.setNormal()
        self.setMutable()
        self.setAcceptDrops(False)
        font = self.font()
        font.fromString(stdfont)
        self.setFont(font)

    def setText(self, text):
        self.setPlainText(text)

    def setMutable(self, mutable=True):
        self.setFlag(self.ItemIsMovable, mutable)
        self.setFlag(self.ItemIsSelectable, mutable)
        if mutable:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction) # allow edits
        else:
            self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction) # disallow edits

    def text(self):
        return self.toPlainText()
        
    def setBrush(self, color):
        self.setDefaultTextColor(color)
        
    def setPos(self, x, y=None):
        if isinstance(x, (QtCore.QPoint, QtCore.QPointF)): # called with point
            x, y = x.x(), x.y()
        x, y = round(x*10)/10, round(y*10)/10
        super(textItem, self).setPos(x, y)

    def toData(self):
        text = self.text()
        if text.startswith('.'):
            return text
        else:
            data = OrderedDict(type='label')
            data['text']   = text
            x, y = self.pos().x(), self.pos().y()
            data['x'] = round(x*10)/10
            data['y'] = round(y*10)/10
            data['anchor'] = self.anchor
            data['font'] = self.font().toString()
            return data

    def fromData(self, data):
        if isinstance(data, dict):
            self.setText(data['text'])
            if 'font' in data:
                font = QtGui.QFont()
                font.fromString(data['font'])
                self.setFont(font)
            if 'anchor' in data:
                self.setAnchor(data['anchor'])
            else:
                self.setAnchor(1)
            self.setPos(data['x'], data['y'])
            self.setNormal()
        else:
            self.setText(data)

    
    def remove(self):
        scene = self.scene()
        scene.removeItem(self)
        
#    def setOrient(self, orient):
#        if orient in 'R0 R45 R90 R135 R180 R225 R270 R315'.split():
#            mirror = 0
#            rot    = float(orient[1:])
#        elif orient in 'MR0 MR45 MR90 MR135 MR180 MR225 MR270 MR315'.split():
#            mirror = 1
#            rot    = float(orient[2:])
#        else:
#            print('unknown orientation')
            
    
    def setFlipped(self):
        '''mirror in place (use when parent is flipped)'''
        self.setTransform(QtGui.QTransform().translate(self.dx, self.dy).scale(-self.scale,self.scale).translate(-self.boundingRect().width(),0))

    def setNormal(self):
        '''normal orientation'''
        self.setTransform(QtGui.QTransform.fromScale(self.scale,self.scale).translate(self.dx, self.dy))
        
    def setAnchor(self, anchor=None):
        if anchor:
            self.anchor = anchor
        if self.anchor in (4,5,6):
            self.dy = -0.5*self.boundingRect().height()
        elif self.anchor in (1,2,3):
            self.dy = -self.boundingRect().height()
        else:
            self.dy = 0

        if self.anchor in (2,5,8):
            self.dx = -0.5*self.boundingRect().width()
        elif self.anchor in (3,6,9):
            self.dx = -self.boundingRect().width()
        else:
            self.dx = 0

class Comment(textItem):
    def __init__(self, text, anchor=1, parent=None):
        super(Comment, self).__init__(text, anchor, parent)
        self.setBrush(colors['comment'])
    
    def toData(self):
        data = super(Comment, self).toData()
        data['type'] = 'comment'
        return data

    def fromData(self, data):
        super(Comment, self).fromData(data)
        # comments do not have an anchor
        self.dx = 0 
        self.dy = 0
        self.setNormal()

def isTextItem(item):
    return isinstance(item, textItem)
    
def isComment(item):
    return isinstance(item, Comment)
    