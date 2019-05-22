# -*- coding: utf-8 -*-
try:
    from odoo import http
    from odoo.http import request
except:
    from openerp import http
    from openerp.http import request

class AppBox(http.Controller):
    @http.route('/appbox/get_session_info', type='json', auth="user")
    def appbox_get_session_info(self):
        session_info = {}
        session_info['appbox_addon_version'] = '1'
        user = request.env.user
        session_info['tz_offset'] = user.tz_offset
        groups_id = user.groups_id.ids
        res = request.env['ir.model.data'].sudo().search_read([('model', '=', 'res.groups'), ('res_id', 'in', groups_id)], ['module', 'name'])
        session_info['groups'] = [group_item['module'] + '.' + group_item['name'] for group_item in res]
        session_info['user_displayname'] = user.display_name
        session_info['company_displayname'] = user.company_id.display_name
        config_items = request.env['app.config'].sudo().search([], limit=1)
        if config_items:
            config_item = config_items[0]
            session_info['app_auth_key'] = config_item.key
        else:
            session_info['app_auth_key'] = ''
        return session_info

    @http.route('/appbox/get_access_rights', type='json', auth="user")
    def appbox_get_access_rights(self, model_list):
        result = {}
        for model in model_list:
            result[model] = {
                'read': request.env['ir.model.access'].check(model, 'read', False),
                'write': request.env['ir.model.access'].check(model, 'write', False),
                'create': request.env['ir.model.access'].check(model, 'create', False),
                'unlink': request.env['ir.model.access'].check(model, 'unlink', False),
            }
        return result

