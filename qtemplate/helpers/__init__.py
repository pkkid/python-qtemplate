# -*- coding: utf-8 -*-
import inspect
import pkgutil
from os.path import dirname, normpath
from PySide6 import QtWidgets
from ..base import QTemplateTag

# Load all QWidget and QTemplateTag classes into __all__ to make
# importing these a bit more straight forward in qtemplate as well
# as not require adding entries from newly created helpers.
__all__ = []
dirpath = normpath(f'{dirname(__file__)}')
for loader, name, ispkg in pkgutil.iter_modules([dirpath]):
    module = loader.find_module(name).load_module(name)
    members = dict(inspect.getmembers(module, lambda obj: (inspect.isclass(obj)
        and obj.__module__ == module.__name__
        and issubclass(obj, (QtWidgets.QWidget, QTemplateTag))
    )))
    for clsname, cls in members.items():
        __all__.append(cls)
