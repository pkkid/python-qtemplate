# -*- coding: utf-8 -*-
from qtemplate.base import QTemplateTag
from qtemplate import utils


class Repeater(QTemplateTag):
    """ Widget-like object used for repeatng child elements in QTemplate.
        <Repeater for='i' in='3'>...</Repeater>
    """

    def __init__(self, qtmpl, elem, parent, context, *args):
        self.qtmpl = qtmpl          # Ref to parent QTemplateWidget object
        self.elem = elem            # Current etree item to render children
        self.parent = parent        # Parent qobj to add children to
        self.context = context      # Context for building the children
        self.varname = None         # Var name for subcontext
    
    def setFor(self, varname):
        self.varname = varname

    def setIn(self, iterable):
        """ Rebuild the children elements on the parent. """
        if self.varname is None:
            raise Exception('Repeater must specify the attribute for before in.')
        if isinstance(iter, str):
            raise Exception(f"Iterable lookup {iterable} failed.")
        utils.deleteChildren(self.parent)
        for item in iterable:
            for echild in self.elem:
                subcontext = dict(**self.context, **{self.varname:item})
                self.qtmpl._walk(echild, self.parent, subcontext)
