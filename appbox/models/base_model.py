# -*- coding: utf-8 -*-
try:
    from odoo import models, api
    from odoo.release import version_info
except:
    from openerp import models, api
    from openerp.release import version_info

origin_fields_get = models.BaseModel.fields_get
def fields_get_old_version(self, cr, user, allfields=None, context=None, write_access=True, attributes=None):
    res = origin_fields_get(self, cr, user, allfields, context, write_access, attributes)
    _all_fields = [self._fields[field_name] for field_name in (res or {}) if self._fields.has_key(field_name)]
    for field_item in _all_fields:
        field_name = field_item.name
        if field_name not in res:
            pass
        elif self._has_onchange(self._fields[field_name], _all_fields):
            res[field_name]['appbox_onchange'] = '1'
        else:
            res[field_name]['appbox_onchange'] = '0'
    return res

@api.model
def fields_get_new_version(self, allfields=None, attributes=None):
    res = origin_fields_get(self, allfields = allfields, attributes = attributes)
    _all_fields = [self._fields[field_name] for field_name in (res or {}) if field_name in self._fields]

    for field_item in _all_fields:
        field_name = field_item.name
        if field_name not in res:
            pass
        elif self._has_onchange(self._fields[field_name], _all_fields):
            res[field_name]['appbox_onchange'] = '1'
        else:
            res[field_name]['appbox_onchange'] = '0'
    return res

if version_info[0] < 10:
    models.BaseModel.fields_get = fields_get_old_version
else:
    models.BaseModel.fields_get = fields_get_new_version