# -*- coding: utf-8 -*-
try:
    from odoo import models, fields, api
except:
    from openerp import models, fields, api

class app_menu(models.Model):
    _name = 'app.menu'
    _order = 'id desc'

    name = fields.Char(string=u"菜单名称", required=True)
    complete_name = fields.Char(string=u"完整路径", compute="_compute_complete_name")
    sequence = fields.Integer(default=10, string=u"菜单顺序", help=u'数字越小优先级越高')
    parent_id = fields.Many2one(comodel_name='app.menu', string=u'上级菜单', default=None)
    action = fields.Reference(selection=[('app.act_window', 'APP窗口动作')], default=None)
    icon = fields.Char(string=u"菜单图标", help=u'填写Awesome图标的名称，如fa-check，仅一级菜单有效。支持4.7.0版本的Awesome图标')
    groups_id = fields.Many2many('res.groups', 'app_menu_group_rel',
                                 'app_menu_id', 'gid', string='Groups',
                                 help=u"指定可访问该菜单的用户组列表，留空表示所有用户都可以访问")

    @api.depends('name', 'parent_id')
    def _compute_complete_name(self):
        for menu_item in self:
            complete_name = menu_item.name or ''
            parent_menu_item = menu_item.parent_id
            while parent_menu_item:
                complete_name = parent_menu_item.name + '/' + complete_name
                parent_menu_item = parent_menu_item.parent_id
            menu_item.complete_name = complete_name
        return 'test'

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        if self.parent_id:
            self.icon = ''

    @api.model
    def get_user_menu_list(self):
        menus = self.search([('action', '!=', False)])
        menus_has_rights = []
        for menu_item in menus:
            try:
                self.env[menu_item.action.res_model].check_access_rights('read')
                menus_has_rights.append(menu_item)
            except:
                continue
        menus = []
        for menu_item in menus_has_rights:
            while menu_item:
                menu = {
                    'id': menu_item.id,
                    'name': menu_item.name,
                    'sequence': menu_item.sequence,
                    'parent_id': menu_item.parent_id.id,
                    'action': self.env['app.act_window'].get_action_data(menu_item.action and menu_item.action.id),
                    'icon': menu_item.icon
                }
                if menu not in menus:
                    menus.append(menu)
                menu_item = menu_item.parent_id
        return menus
