# -*- coding: utf-8 -*-
{
    'name': "appbox config for sale_order",

    'summary': """
        AppBox configuration for sale_order""",

    'description': """
        Android App: https://play.google.com/store/apps/details?id=com.odooappbox
        iPhone App: https://apps.apple.com/us/app/odooappbox/id1465496744
    """,

    'author': "You Zengjian",
    'website': "https://github.com/youzengjian/OdooAppBox",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0.0',

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