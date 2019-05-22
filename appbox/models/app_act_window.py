# -*- coding: utf-8 -*-
import sys
try:
    from odoo import models, fields, api
except:
    from openerp import models, fields, api

class app_act_window(models.Model):
    _name = 'app.act_window'

    name = fields.Char(string=u"动作名称")
    res_model = fields.Char(string=u"目标模型")
    target = fields.Selection(selection=[('new', u'新窗口'), ('self', u'当前窗口')],
                              string=u'目标窗口', default='self', required=True)
    view_mode = fields.Char(string=u"允许的视图模式", default='kanban,form', required=True)
    view_kanban = fields.Many2one(comodel_name='app.view', string=u'看板视图', domain="[('type', '=', 'kanban')]")
    view_form = fields.Many2one(comodel_name='app.view', string=u'表单视图', domain="[('type', '=', 'form')]")
    view_search = fields.Many2one(comodel_name='app.view', string=u'搜索视图', domain="[('type', '=', 'search')]")
    domain = fields.Char(string=u"过滤条件")
    context = fields.Char(string=u"上下文值", required=True, default='{}')
    options = fields.Char(string=u"高级选项", default='{}')

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