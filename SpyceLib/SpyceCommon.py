#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 16:49:35 2020

@author: paul
"""
from preferences import GRID
from Qt.QtCore import QPointF # see https://github.com/mottosso/Qt.py

#==============================================================================
# snap to grid
#==============================================================================
def gridPos(pt):
     gr = GRID
     x = gr * ((pt.x() + gr /2) // gr)
     y = gr * ((pt.y() + gr /2) // gr)
     return QPointF(x,y)
