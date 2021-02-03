#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# =============================================================================
# compile resource file or ui file
# =============================================================================
"""
import os, sys, shutil
from pathlib    import Path
from subprocess import Popen, PIPE

QT_PREFERRED_BINDING = ['PyQt5', 'PySide2', 'PyQt4']


#check python >= 3.3
if sys.version_info[0] < 3 or sys.version_info[1] < 3:
    print('This program needs python 3.3 or newer')
    sys.exit()

log = sys.stdout # default log function == write to stdout
err = sys.stderr # default error function == write to stderr
def errprint(*args, **kwargs):
    kwargs['file'] = err # override output
    print(*args, **kwargs)
    logprint(*args, **kwargs)# also echo in log
              
def logprint(*args, **kwargs):
    kwargs['file'] = log # override output
    print(*args, **kwargs)

# check if there is already loaded Qt version
if 'QT_PREFERRED_BINDING' not in os.environ:
    mods = ' '.join(list(sys.modules.keys()))
    for k in QT_PREFERRED_BINDING:
        if k in mods:
            os.environ['QT_PREFERRED_BINDING'] = k
            break
    else: # nothing found
        os.environ['QT_PREFERRED_BINDING'] = os.pathsep.join(QT_PREFERRED_BINDING)


import Qt  # see https://github.com/mottosso/Qt.py

    
if Qt.__binding__ in ['PyQt5', 'PySide2', 'PyQt4']:
    logprint('using {} binding'.format(Qt.__binding__))
else:
    errprint('No Qt binding available.')
    errprint('This tool needs either PyQt5 or PySide2 (PyQt4 might work, but is end-of-life and no longer maintained)')
    errprint('exiting')
    sys.exit()

# fix missing import in Qt.Py
if Qt.__binding__ == 'PyQt5':
    from PyQt5.QtWidgets import QProxyStyle as _QProxyStyle
elif Qt.__binding__ == 'PySide2':
    from PySide2.QtWidgets import QProxyStyle as _QProxyStyle
elif Qt.__binding__ == 'PyQt4':
    from PyQt4.QtWidgets import QProxyStyle as _QProxyStyle
Qt.QtWidgets.QProxyStyle = _QProxyStyle



def QtCompile(src, dest, forceRecompile=False):
    p = os.path.dirname(os.path.dirname(__file__)) # one directory up from this file
    
    src = os.path.join(p, "QtDesignerFiles", src)
    dest = os.path.join(p, dest)

    if Qt.__binding__ =='PyQt5':
        uic, rcc, deb_pkg, pip_pkg = 'pyuic5', 'pyrcc5', 'pyqt5-dev-tools', 'pyqt5'
    elif Qt.__binding__ =='PySide2':
        uic, rcc, deb_pkg , pip_pkg = 'pyside2-uic', 'pyside2-rcc', 'pyside2-tools', 'pyside2'
    elif Qt.__binding__ =='PyQt4':
        uic, rcc, deb_pkg, pip_pkg  = 'pyuic4', 'pyrcc4', 'pyqt4-dev-tools', ''
        errprint('Note that Qt4 no longer maintained. You should consider upgrading to PyQt5 or Pyside2')
    
    if src.endswith(".qrc"): 
        exe = shutil.which(rcc)
    elif src.endswith(".ui"): 
        exe = shutil.which(uic)
    else:
        raise("unknown qt extension", src)
        
    if exe:
        destdir = os.path.dirname(dest)
        if destdir and not os.path.exists(destdir):
            os.makedirs(destdir)
            Path(os.path.join(destdir, "__init__.py")).touch()
        
        if not os.path.exists(dest) or forceRecompile or \
               os.path.getmtime(src) >  os.path.getmtime(dest):
            logprint('(re)compiling {}'.format(src))
            if Qt.__binding__ =='PyQt5' or src.endswith(".qrc"):
                cmd = [exe] + ['-o', dest, src]
            else: # forces current interpreter rather than default python (often py2)
                cmd = [sys.executable, exe] + ['-o', dest, src] 
            proc = Popen(cmd, stderr=PIPE)
            out, err = proc.communicate()
            if err:
                msg = err.decode("utf-8")
                errprint("Error: {}\nwhile executing '{}'".format(msg, ' '.join(cmd)))
                sys.exit()
                
        if Qt.__binding__ =='PySide2': # need to fix all pyside2 imports
            with open(dest) as f:
                lines = Qt._convert(f.readlines())

            backup = "%s_backup%s" % os.path.splitext(dest)
            logprint("Creating '%s'.." % backup)
            shutil.copy(dest, backup)
        
            with open(dest, "w") as f:
                f.write("".join(lines))
    
            logprint("Successfully converted '{}'".format(dest))



            
    else:
        errprint('Qt tool {} cannot be found. Make sure it is in the execution path'.format(exe))
        errprint("You can install it with 'apt install {}' (Linux debian/ubuntu)".format(deb_pkg))
        if pip_pkg:
            errprint("Alternatively you can use 'pip install {}'".format(pip_pkg))
        errprint('exiting')
        sys.exit()

