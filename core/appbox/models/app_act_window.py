# -*- coding: utf-8 -*-
import sys
try:
    from odoo import models, fields, api
except:
    from openerp import models, fields, api

class app_act_window(models.Model):
    _name = 'app.act_window'

    name = fields.Char(string=u"Action Name", translate=True)
    res_model = fields.Char(string=u"Object")
    target = fields.Selection(selection=[('new', u'New Window'), ('self', u'Current Window')],
                              string=u'Target Window', default='self', required=True)
    view_mode = fields.Char(string=u"View Mode", default='kanban,form', required=True)
    view_kanban = fields.Many2one(comodel_name='app.view', string=u'Kanban View', domain="[('type', '=', 'kanban')]")
    view_form = fields.Many2one(comodel_name='app.view', string=u'Form View', domain="[('type', '=', 'form')]")
    view_search = fields.Many2one(comodel_name='app.view', string=u'Search View', domain="[('type', '=', 'search')]")
    domain = fields.Char(string=u"Domain Value")
    context = fields.Char(string=u"Context Value", required=True, default='{}')
    options = fields.Char(string=u"Options Value", default='{}')

    @api.model
    def get_action_data(self, action_id):
        def is_str(value):
            if sys.version_info[0] < 3:
                return isinstance(value, basestring)
            else:
                return isinstance(value, str)
        if is_str(action_id):
            action = self.env['ir.model.data'].xmlid_to_object(action_id)
        elif isinstance(action_id, int):
            action = self.browse(action_id)
        else:
            action = None

        if action:
            return action.read()[0]
        else:
            return {}