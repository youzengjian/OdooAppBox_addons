# -*- coding: utf-8 -*-
try:
    from odoo import models, fields, api
except:
    from openerp import models, fields, api

class app_menu(models.Model):
    _name = 'app.menu'
    _order = 'id desc'

    name = fields.Char(string=u"Menu", required=True, translate=True)
    complete_name = fields.Char(string=u"Full Path", compute="_compute_complete_name")
    sequence = fields.Integer(default=10, string=u"Sequence", help=u'Defines the order of menu, lower values mean higher priority')
    parent_id = fields.Many2one(comodel_name='app.menu', string=u'Parent Menu', default=None)
    action = fields.Reference(selection=[('app.act_window', 'Action')], default=None)
    icon = fields.Char(string=u"Icon", help=u'Font Awesome(Version 4.7.0) icon name. eg:fa-check. Valid for root menu.')
    groups_id = fields.Many2many('res.groups', 'app_menu_group_rel','app_menu_id', 'gid', string='Groups',
                                 help="If you have groups, the visibility of this menu will be based on these groups and related object's read access." \
                                      "If this field is empty, Odoo will compute visibility based on the related object's read access.")

    @api.depends('name', 'parent_id')
    def _compute_complete_name(self):
        for menu_item in self:
            complete_name = menu_item.name or ''
            parent_menu_item = menu_item.parent_id
            while parent_menu_item:
                complete_name = parent_menu_item.name + '/' + complete_name
                parent_menu_item = parent_menu_item.parent_id
            menu_item.complete_name = complete_name
        return ''

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
