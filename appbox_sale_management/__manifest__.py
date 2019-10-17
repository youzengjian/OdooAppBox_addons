# -*- coding: utf-8 -*-
{
    'name': "appbox_sale_management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'appbox', 'appbox_base', 'appbox_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/app_view_account_invoice.xml',
        'data/app_view_account_voucher.xml',
        'data/app_view_res_partner.xml',
        'data/app_view_sale_advance_payment_inv.xml',
        'data/app_view_sale_order.xml',
        'data/app_action.xml',
        'data/app_menu.xml',
    ],
    'application': True,
}