#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:51:50 2021

@author: paul
"""
import sys
import ast
from collections import OrderedDict

from SpyceLib.misc import QtCompile

QtCompile("propertiesDialog.ui", 'Ui/propertiesDialog.py', forceRecompile=True)
from Ui.propertiesDialog import Ui_propertiesDialog

from Qt.QtCore    import Qt
from Qt.QtGui     import (QStandardItemModel, QStandardItem, QCursor)
from Qt.QtWidgets import (QHeaderView, QStyleOption, QMenu, QAction, 
                          QDialog, QProxyStyle, QApplication, QComboBox, 
                          QAbstractItemView, QCheckBox)

# =============================================================================
# enhanced widgets (needed for Drag & Drop)
# =============================================================================
class myComboBox(QComboBox):
    def __init__(self, ix_values):
        '''val : [ix, (item0, item1, item...)]'''
        QComboBox.__init__(self)
        ix, values = ix_values
        self.types = [type(i) for i in values]
        self.addItems([str(item) for item in values])
        self.setCurrentIndex(ix)
        self.setAutoFillBackground(True)
        
    def __repr__(self):
        ix = self.currentIndex()
        data = [self.itemText(i) for i in range(self.count())]
        return repr([ix, tuple(data)])
    
    @property
    def value(self):
        '''return the value (same type as original)'''
        ix = self.currentIndex()
        data = [self.types[i](self.itemText(i)) for i in range(self.count())]
        return [ix, tuple(data)]
        
    
class myCheckBox(QCheckBox):
    def __init__(self, state):
        super().__init__()
        if state:
            self.setCheckState(Qt.Checked)
        else:
            self.setCheckState(Qt.Unchecked)
        self.setTristate(False)
        self.setAutoFillBackground(True)
        
    def __repr__(self):
        state = 'True' if self.checkState() else 'False'
        return state

    @property
    def value(self):
        return self.checkState()>0
    
class myStandardItem(QStandardItem):
    def __init__(self, val):
        super().__init__(f'{val}')
        self._type = type(val)
        
    @property
    def value(self):
        return self.checkState()>0
       
    
# =============================================================================
# custom model to be able to drag and drop a whole row (with widgets)
# =============================================================================
class customModel(QStandardItemModel):
    """
    custom model to allow for drag & drop without column "shifting"
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.keep = [] # store the current row widgets during a drag
        
    def myWidget(self, val):
        '''
        this function returns a widget depending on val
           [ix, (option0, option1 ... optionn)] -> ComboBox
           bool (True/False)                    -> CheckBox'''
        if isinstance(val, (list, tuple)):
            w = myComboBox(val)
            w.setAutoFillBackground(True)
            return w
        elif isinstance(val, bool):
            w = myCheckBox(val)
            w.setAutoFillBackground(True)
            return w
        else:
            return None 

    def mimeData(self,indices):
        """
        Move all data, including hidden/disabled columns
        """

        index = indices[0] # only the first one!
        row = index.row()
        new_data = []
        for col in range(self.columnCount()):
            ix = index.sibling(row, col)
            new_data.append(ix) 
            
            widget = self.parent().indexWidget(ix)
            if widget:
                self.keep.append(repr(widget))
            else:
                self.keep.append('')
        
        return super().mimeData(new_data)

    def dropMimeData(self, data, action, row, col, parent):
        """
        (action should always be Qt.MoveAction==2)
        Always move the entire row, and don't allow column "shifting"
        """
        response = super().dropMimeData(data, Qt.CopyAction, row, 0, parent)
        if self.keep:
            for col in range(self.columnCount()):
                s = self.keep[col]
                if s:
                    val = ast.literal_eval(s)
                    cb = self.myWidget(val)
                    ix = self.index(row, col)
                    self.parent().setIndexWidget(ix, cb)
            self.keep = []

        return response

    def populate(self, properties, headers):
        for ix, (name, values) in enumerate(properties.items()):
            data = [QStandardItem(f'{name}')]#, QStandardItem(f'{values}')]
            data[0].setDropEnabled(False)
            data[0].setEditable(False)
            for val in values:
                item = QStandardItem(f'{val}')
                item.setDropEnabled(False)
                data.append(item)
            self.appendRow(data)
            for c, val in enumerate(values):
                i = self.index(ix, c+1)
                cb = self.myWidget(val)
                if cb:
                    self.parent().setIndexWidget(i, cb)
        if headers:
            self.setHorizontalHeaderLabels(headers)
        h = self.parent().horizontalHeader()       
        h.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.Stretch)


class customStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        """
        Draw a line across the entire row rather than just the column
        we're hovering over."""
        if element == self.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            option_new = QStyleOption(option)
            option_new.rect.setLeft(0)
            if widget:
                option_new.rect.setRight(widget.width())
            option = option_new
        super().drawPrimitive(element, option, painter, widget)



class propertiesDialog(QDialog, Ui_propertiesDialog):
    """
    Properties dialog class
    """
    def __init__(self, properties, headers=None, mode='adri'):
        """
        mode a: allow add
        mode d: allow delete
        mode r: allow reorder
        mode i: force name to be valid identifier
        """
        super().__init__()
        self.setupUi(self)     
        self.properties = OrderedDict(properties)
        self.mode = mode
        # set to cursor position
        # will place window in current screen, even when cursor at some 'odd location'
        rect = self.geometry()
        rect.moveTo(QCursor.pos())
        self.setGeometry(rect) # will place window in current screen, even when at some 'odd location'
        
        self.propertiesTableView.setStyle(customStyle())        
        model = customModel(parent=self.propertiesTableView)
        self.propertiesTableView.setModel(model)

        self.row = -1
        if 'd' in self.mode:
            self.propertiesTableView.customContextMenuRequested.connect(self.showContextMenu)
        if 'a' in self.mode:
            self.addProperty.clicked.connect(self.addRow)
        else:
            self.addProperty.hide()
        if 'r' in mode:
            self.propertiesTableView.setDragDropMode(QAbstractItemView.InternalMove)

        # push buttons signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        model.populate(self.properties, headers)


    def showContextMenu(self, pos):
        self.row = self.propertiesTableView.indexAt(pos).row()
        self.menu = QMenu(self)
        deleteRowAction = QAction('Delete', self)
        deleteRowAction.triggered.connect(self.deleteRow)
        self.menu.addAction(deleteRowAction)
        # add other required actions
        self.menu.popup(QCursor.pos())
        
    def deleteRow(self):
        model = self.propertiesTableView.model()
        model.removeRows(self.row, 1)
        
    def addRow(self):
        model = self.propertiesTableView.model()
        data = [QStandardItem('') for i in range(model.columnCount())]
        for d in data:
            d.setDropEnabled(False)
        model.appendRow(data)
        
    def accept(self):
        print('OK')
        model =  self.propertiesTableView.model()
        
        new_properties = OrderedDict()

        for row in range(model.rowCount()):
            values = []
            name = model.data(model.index(row,0))
            for col in range(1, model.columnCount()):
                ix = model.index(row, col)
                widget = self.propertiesTableView.indexWidget(ix)
                if widget:
                    value = widget.value
                else:
                    value = model.data(model.index(row,col)) # string type
                    if name in self.properties: # restore original type
                        value = type(self.properties[name][col-1])(value)
                values.append(value)

            name = str(name).strip()
            if 'i' in self.mode:
                if name.isidentifier(): # valid name
                    new_properties[name] = values
            elif name:
                    new_properties[name] = values

        self.properties = new_properties
        super().accept()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    pp = OrderedDict()
    pp['een']      = [1]
    pp['twee']     = ['twee']
#    pp['fortytwo'] = 'twee en veertig'
    pp['fortytwo'] = [[0, ('twee en veertig', 42, '0x28')]]
    pp['Noo']      = [False]
    for name in pp:
        pp[name].append(True)
    headers = 'Name Value Visible'.split()        
    window = propertiesDialog(pp, headers)
    res = window.exec_()
    print(window.properties)

    # pin dialog
    pp = OrderedDict()
    pp['A1'] = [-40, 0,  [0, ('input', 'output', 'inout')]]
    pp['A2'] = [-40, 10, [0, ('input', 'output', 'inout')]]
    pp['A3'] = [-40, 20, [0, ('input', 'output', 'inout')]]
    pp['A4'] = [-40, 30, [0, ('input', 'output', 'inout')]]
    pp['Z']  = [ 40, 10, [1, ('input', 'output', 'inout')]]
    pp['ZN'] = [ 40, 20, [1, ('input', 'output', 'inout')]]
    headers = ['Name', 'X', 'Y', 'pin Type']

    window = propertiesDialog(pp, headers)
    res = window.exec_()
    print(window.properties)

#    sys.exit(app.exec_())