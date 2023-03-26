# -*- coding: utf-8 -*-
import sass
from os.path import dirname, normpath, isabs
from PySide6 import QtCore
from qtemplate.base import QTemplateTag
from string import Template


class StyleSheet(QTemplateTag):
    """ Widget-like object used for importing and applying stylesheets.
        <StyleSheet args='<path>' context='<dict>'/>
    """

    def __init__(self, qtmpl, elem, parent, context, *args):
        self.qtmpl = qtmpl          # Ref to parent QTemplateWidget object
        self.elem = elem            # Current etree item to render children
        self.parent = parent        # Parent qobj to add children to
        self.context = context      # Context for building the children
        self.filepath = args[0]     # Relative path to stylesheet (from tmpl)
        if 'context' not in self.elem.attrib:
            self.setContext()

    def setContext(self, context=None):
        context = context or {}
        filepath = normpath(self.filepath)
        if not isabs(filepath):
            filepath = normpath(f'{dirname(self.qtmpl.filepath)}/{self.filepath}')
        context.update({'dir': dirname(filepath).replace('\\','/')})
        template = Template(open(filepath).read())
        styles = template.safe_substitute(context)
        styles = sass.compile(string=styles)
        if QtCore.QCoreApplication.instance().opts.outline:
            styles += 'QWidget { border:1px solid rgba(255,0,0,0.3) !important; }'
        self.parent.setStyleSheet(styles)
