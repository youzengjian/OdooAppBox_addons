# -*- coding: utf-8 -*-
import sys
from lxml import etree
import copy
from lxml.builder import E

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

try:
    from odoo import models, fields, api, _
    from odoo.tools.translate import xml_translate, TRANSLATED_ATTRS
except:
    from openerp import models, fields, api
    xml_translate = False


class app_view(models.Model):
    _name = 'app.view'
    _order = "priority,name,id"

    name = fields.Char(string=u"View name", required=True, translate=True)
    res_model = fields.Char(string=u"Model", required=True)
    type = fields.Selection(string=u"View Type", selection=[('kanban', 'Kanban'), ('form', 'Form'), ('search', 'Search')], required=True)
    arch_original = fields.Text(string=u"Architecture", required=True, translate=xml_translate)
    arch = fields.Text(string=u"Architecture", compute='_compute_arch')
    inherit_id = fields.Many2one('app.view', string='View inheritance', ondelete='restrict')
    inherit_children_ids = fields.One2many('app.view', 'inherit_id', string='inherited Views')
    priority = fields.Integer(string='Sequence', help="lower values mean higher priority.", default=16, required=True)

    @api.onchange('arch_original')
    def onchang_arch_original(self):
        if self.arch_original:
            # Ensure arch_original is valid xml content
            etree.fromstring(self.arch_original)

    @api.depends('arch_original')
    def _compute_arch(self):
        def add_text_inside(node, text):
            """ Add text inside ``node``. """
            if text is None:
                return
            if len(node):
                node[-1].tail = (node[-1].tail or "") + text
            else:
                node.text = (node.text or "") + text

        def add_text_before(node, text):
            """ Add text before ``node`` in its XML tree. """
            if text is None:
                return
            prev = node.getprevious()
            if prev is not None:
                prev.tail = (prev.tail or "") + text
            else:
                parent = node.getparent()
                parent.text = (parent.text or "") + text

        def remove_element(node):
            """ Remove ``node`` but not its tail, from its XML tree. """
            add_text_before(node, node.tail)
            node.tail = None
            node.getparent().remove(node)

        def compine_view_by_xpath(view_arch, xpath_arch):
            view_arch_tree = etree.fromstring(view_arch)
            xpath_tree = etree.fromstring(xpath_arch)
            if xpath_tree.tag != 'data':
                raise Exception(_("Inherited view's root element must be 'data'."))
            for xpath_element in xpath_tree:
                if xpath_element.tag != 'xpath':
                    continue

                expr = xpath_element.get('expr', None)
                if expr is None:
                    raise Exception(_('The expr attribute of an xpath element cannot be empty.'))
                nodes = etree.ETXPath(expr)(view_arch_tree)
                node = nodes[0] if nodes else None
                if node is None:
                    raise Exception(_("Element cannot be located in parent view, XPATH Expression:") + expr)

                pos = xpath_element.get('position', 'inside')
                if pos == 'replace':
                    if node.getparent() is None:
                        raise Exception(_('You cannot perform a replacement operation on the root node of the parent view.'))
                    else:
                        for child in xpath_element:
                            node.addprevious(child)
                        node.getparent().remove(node)
                elif pos == 'attributes':
                    for child in xpath_element.getiterator('attribute'):
                        attribute = child.get('name')
                        value = child.text or ''
                        node.set(attribute, value)
                elif pos == 'inside':
                    add_text_inside(node, xpath_element.text)
                    for child in xpath_element:
                        node.append(child)
                elif pos == 'after':
                    # add a sentinel element right after node, insert content of
                    # spec before the sentinel, then remove the sentinel element
                    sentinel = E.sentinel()
                    node.addnext(sentinel)
                    add_text_before(sentinel, xpath_element.text)
                    for child in xpath_element:
                        sentinel.addprevious(child)
                    remove_element(sentinel)
                elif pos == 'before':
                    add_text_before(node, xpath_element.text)
                    for child in xpath_element:
                        node.addprevious(child)
                else:
                    self.raise_view_error(_("Unsupported pos attribute:") + pos)
            return etree.tostring(view_arch_tree, encoding='utf-8')

        def combine_view(view_arch, child_view, recursion):
            view_arch = compine_view_by_xpath(view_arch, child_view.arch_original)
            if not recursion:
                return view_arch
            for view in child_view.inherit_children_ids:
                view_arch = combine_view(view_arch, view, recursion)
            return view_arch

        root = self
        view_ids = []
        while root.inherit_id:
            root = root.inherit_id
            if root.inherit_id:
                view_ids.append(root)

        ret = root.arch_original
        for view in view_ids:
            ret = combine_view(ret, view, False)

        if root == self:
            for view in root.inherit_children_ids:
                ret = combine_view(ret, view, True)
        else:
            ret = combine_view(ret, self, True)
        self.arch = ret
