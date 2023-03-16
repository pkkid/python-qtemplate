# -*- coding: utf-8 -*-
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class DraggableMixin:
    """ Draggable Mixin, allows specifying a parent window to be moved. """

    def __init__(self, window=None):
        self.window = self if window is None else window
        self._dragMousePos = None
        self._dragWidgetPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragMousePos = event.globalPos()
            self._dragWidgetPos = self.window.pos()

    def mouseMoveEvent(self, event):
        if self._dragMousePos:
            delta = event.globalPos() - self._dragMousePos
            self.window.move(self._dragWidgetPos + delta)
                
    def mouseReleaseEvent(self, event):
        if self._dragMousePos:
            delta = event.globalPos() - self._dragMousePos
            if (delta.x() != 0 or delta.y() != 0) and hasattr(self, 'widgetMoved'):
                self.widgetMoved(self.pos())
        self._dragMousePos = None
        self._dragWidgetPos = None


class Draggable(DraggableMixin, QtWidgets.QWidget):
    """ Draggable QWidget, allows specifying a parent window to be moved. """

    def __init__(self, window=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, *args, **kwargs)
        DraggableMixin.__init__(self, window)
