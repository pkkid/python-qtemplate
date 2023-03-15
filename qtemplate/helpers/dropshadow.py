# -*- coding: utf-8 -*-
from PySide6 import QtGui, QtWidgets
from qtemplate.base import QTemplateTag


class DropShadow(QTemplateTag):
    """ Applies a dropshadow to the parent element. """
    
    def __init__(self, qtmpl, elem, parent, context, *args):
        # Read the args (x, y, blur, opacity{0-255})
        x = args[0] if len(args) >= 1 else 0
        y = args[1] if len(args) >= 2 else 0
        blur = args[2] if len(args) >= 3 else 0
        opacity = args[3] if len(args) >= 4 else 255
        # Create the shadow effect and apply it to parent
        # We save the effect object to parent so it's not garbage collected
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setOffset(x, y)
        shadow.setBlurRadius(blur)
        shadow.setColor(QtGui.QColor(0, 0, 0, opacity))
        parent.setGraphicsEffect(shadow)
        parent._dropshadow = shadow  # icky
        # Set grandparent's margins to allow space for dropshadow
        parent.parent().setContentsMargins(*[max(x,y)+blur]*4)
