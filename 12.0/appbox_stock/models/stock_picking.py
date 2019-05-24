# -*- coding: utf-8 -*-
import sys
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')

try:
    from odoo import models, fields, api
except:
    from openerp import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def app_button_validate(self):
        ret = self.button_validate()
        if (ret):
            if (ret.get('view_id') == self.env.ref('stock.view_immediate_transfer').id):
                ret['type'] = 'app.act_window'
                ret['view_id'] = self.env.ref('appbox_stock.app_view_immediate_transfer').id
            elif (ret.get('view_id') == self.env.ref('stock.view_overprocessed_transfer').id):
                ret['type'] = 'app.act_window'
                ret['view_id'] = self.env.ref('appbox_stock.app_view_overprocessed_transfer').id
            elif (ret.get('view_id') == self.env.ref('stock.view_backorder_confirmation').id):
                ret['type'] = 'app.act_window'
                ret['view_id'] = self.env.ref('appbox_stock.app_view_backorder_confirmation').id
        else:
            pass
        return ret


