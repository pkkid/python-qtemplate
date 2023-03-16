# -*- coding: utf-8 -*-
import re
import sass
from collections import OrderedDict
from qtemplate import log


class Bunch(OrderedDict):
    """ Allows dot notation to set and get dict values. """
    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            return None

    def __setattr__(self, item, value):
        return self.__setitem__(item, value)


def deleteChildren(qobj):
    """ Delete all children of the specified QObject. """
    if hasattr(qobj, 'clear'):
        return qobj.clear()
    layout = qobj.layout()
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget: widget.deleteLater()
        else: deleteChildren(item.layout())


def rget(obj, attrstr, default=None, delim='.'):
    """ Recursively get a value from a nested dictionary. """
    try:
        attr, *substr = attrstr.split(delim, 1)
        if isinstance(obj, dict):
            if attr == 'keys()': value = obj.keys()
            elif attr == 'values()': value = obj.values()
            else: value = obj[attr]
        elif isinstance(obj, list): value = obj[int(attr)]
        elif isinstance(obj, tuple): value = obj[int(attr)]
        elif isinstance(obj, object): value = getattr(obj, attr)
        if substr: return rget(value, '.'.join(substr), default, delim)
        return value
    except Exception as err:
        log.warning(err, exc_info=True)
        return default


def rset(obj, attrstr, value, delim='.'):
    """ Recursively set a value to a nested dictionary. """
    parts = attrstr.split(delim, 1)
    attr = parts[0]
    attrstr = parts[1] if len(parts) == 2 else None
    if attrstr and attr not in obj:
        obj[attr] = Bunch() if isinstance(obj, Bunch) else {}
    if attrstr:
        return rset(obj[attr], attrstr, value)
    obj[attr] = value


def setStyleSheet(qobj, filepath, context=None, outline=False):
    """ Load the specified stylesheet via libsass and add it to qobj. """
    styles = open(filepath).read()
    styles = sass.compile(string=styles)
    if outline:
        styles += 'QWidget { border:1px solid rgba(255,0,0,0.3) !important; }'
    qobj.setStyleSheet(styles)


def typeStr(value):
    """ Return the type of value as a string. """
    return re.findall(r"(\w+?)\'", str(type(value)))[0].lower()
