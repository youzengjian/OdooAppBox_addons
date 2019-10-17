# -*- coding: utf-8 -*-
try:
    from odoo import http
    from odoo.release import version_info
except:
    from openerp import http
    from openerp.release import version_info

origin_authenticate = http.OpenERPSession.authenticate
def authenticate_new(self, db, login=None, password=None, uid=None):
    uid = origin_authenticate(self, db=db, login=login, password=password, uid=uid)
    if self.rotate:
        http.root.session_store.delete(self)
        self.sid = http.root.session_store.generate_key()
        self.rotate = False
        from odoo.service import security
        self.session_token = security.compute_session_token(self, http.request.env)
        http.root.session_store.save(self)
    return uid

if version_info[0] >= 12:
    http.OpenERPSession.authenticate = authenticate_new
