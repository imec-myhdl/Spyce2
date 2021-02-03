from __future__ import print_function
import os, sys
from collections import OrderedDict
    
# defaults for icon creation
# icons use QFont("Helvetica", 14, QFont.Normal) 
icon_font_size = 10  # height
icon_pin_size  = 10 # length of line segment (starting at pin-position)
icon_cache_dir = '.iconcache'
netlist_dir    = 'netlist' #path for netlists
    
#pycmd = 'ipython3 qtconsole &'
pycmd = 'jupyter qtconsole &'
pyrun = 'python'

#==============================================================================
# Netlisting
#==============================================================================
projectname      = 'projectname placeholder'
version          = '1.0'
copyrightText    = 'copyright placeholder'
copyrightPolicy  = 'copyright policy placeholder'
ticks_per_second = 1e15 # ticks per second
t_stop           = 1e-6 # simulation stop time


#==============================================================================
# GUI preferences
#==============================================================================

GRID  = 10  # grid spacing
PW    = 8   # pin width
PD    = 20  # pin distance (spacing between pins in blocks)
NW    = 4   # node width
LW    = 2   # line width for connection
BWmin = 80  # block minimum width
BHmin = 60  # block minimum height
DB    = 2   # selection radius (dynamically scaling with zoom)

stdfont = 'Sans Serif,12' # used for (pin)labels/comments
#==============================================================================
# predefined colors
# Qt.white       3  White (#ffffff)
# Qt.black       2  Black (#000000)
# Qt.red         7  Red (#ff0000)
# Qt.darkRed     13 Dark red (#800000)
# Qt.green       8  Green (#00ff00)
# Qt.darkGreen   14 Dark green (#008000)
# Qt.blue        9  Blue (#0000ff)
# Qt.darkBlue    15 Dark blue (#000080)
# Qt.cyan        10 Cyan (#00ffff)
# Qt.darkCyan    16 Dark cyan (#008080)
# Qt.magenta     11 Magenta (#ff00ff)
# Qt.darkMagenta 17 Dark magenta (#800080)
# Qt.yellow      12 Yellow (#ffff00)
# Qt.darkYellow  18 Dark yellow (#808000)
# Qt.gray        5  Gray (#a0a0a4)
# Qt.darkGray    4  Dark gray (#808080)
# Qt.lightGray   6  Light gray (#c0c0c0)
#==============================================================================
colors = dict() 
if 'Qt'in sys.modules: # needed to import without gui
    from Qt import QtCore
#                           (line,               fill)
    colors['port_input']  = (QtCore.Qt.black,    QtCore.Qt.black)
    colors['port_output'] = (QtCore.Qt.black,    QtCore.Qt.black)
    colors['port_inout']  = (QtCore.Qt.black,    QtCore.Qt.black)
    colors['port_ipin']   = (QtCore.Qt.black,    QtCore.Qt.darkRed)
    colors['port_opin']   = (QtCore.Qt.black,    QtCore.Qt.darkRed)
    colors['port_iopin']  = (QtCore.Qt.black,    QtCore.Qt.darkRed)
    colors['node']        = (QtCore.Qt.darkBlue, QtCore.Qt.darkBlue)
    colors['block']       =  QtCore.Qt.darkGreen # no fill color
    colors['connection']  =  QtCore.Qt.darkBlue  # no fill color
    colors['comment']     =  QtCore.Qt.darkGray  # no fill color
    colors['signalType']  =  QtCore.Qt.darkGray  # no fill color


#==============================================================================
# view editors:
#==============================================================================
textEditor        = 'kate'
codeEditor        = 'kate'
officeEditor      = 'libreoffice --writer'
pythonEditor      = 'spyder3'

viewTypes    = OrderedDict()
#          viewtype          (editor          extension   )
viewTypes['diagram']       = (codeEditor,    '.diagram'   )
viewTypes['myhdl']         = (codeEditor,    '.myhdl'     )
viewTypes['blk_source']    = (pythonEditor,  '.py'        )
viewTypes['text']          = (textEditor,    '.txt'       )
viewTypes['vhdl']          = (codeEditor,    '.vhd'       )
viewTypes['systemverilog'] = (codeEditor,    '.sv'        )
viewTypes['verilog']       = (codeEditor,    '.v'         )
viewTypes['doc']           = (officeEditor,  '.odt'       )
#==============================================================================
#if os.path.isfile('settings.py'):
#    from settings import *
#    if 'templates' in locals():
#        _templates.update(templates)
#
#templates = _templates
        