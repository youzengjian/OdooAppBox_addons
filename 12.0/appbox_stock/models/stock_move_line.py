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

    qty_need_scan = fields.Float(string="Reserved", compute='_compute_qty_need_scan', digits=(16, 0))
    qty_scanned = fields.Float(string="Done", default=0.0, digits=(16, 0))

    @api.depends('qty_done', 'product_uom_qty', 'picking_id')
    def _compute_qty_need_scan(self):
        for line_item in self:
            line_item.qty_need_scan = line_item.product_uom_qty

    @api.model
    def create(self, values):
        if values.get('qty_scanned'):
            values['qty_done'] = values['qty_scanned']
            values['done_wo'] = False
        return super(StockMoveLine, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('qty_scanned'):
            values['qty_done'] = values['qty_scanned']
        return super(StockMoveLine, self).write(values)