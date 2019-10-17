# -*- coding: utf-8 -*-
import sys
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

try:
    from odoo import models, fields, api
except:
    from openerp import models, fields, api

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    qty_need_scan = fields.Float('Reserved', compute='_compute_qty_need_scan', digits=(16, 0))

    @api.depends('qty_done', 'product_uom_qty', 'picking_id', 'workorder_id')
    def _compute_qty_need_scan(self):
        for line_item in self:
            if line_item.workorder_id:
                line_item.qty_need_scan = line_item.qty_done
            else:
                line_item.qty_need_scan = line_item.product_uom_qty
