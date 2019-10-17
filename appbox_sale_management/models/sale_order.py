# -*- coding: utf-8 -*-
try:
    from odoo import models, api, _
except:
    from openerp import models, api

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def app_action_view_invoices(self):
        result = {
            'name': _('Invoices'),
            'type': 'app.act_window',
            'res_model': 'account.invoice',
            'target': 'self',
            'view_mode': 'kanban,form',
            'view_form': self.env.ref('appbox_sale_management.app_view_account_invoice_form').id,
            'context': '{}',
            'options': '{}'
        }
        inv_ids = []
        for sale_order_item in self:
            inv_ids += [invoice.id for invoice in sale_order_item.invoice_ids]

        if len(inv_ids)>1:
            result['domain'] = "[('id','in',["+','.join(map(str, inv_ids))+"])]"
        else:
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result