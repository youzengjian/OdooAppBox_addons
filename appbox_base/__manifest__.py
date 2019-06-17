# -*- coding: utf-8 -*-
{
    'name': "appbox config for res_partner",

    'summary': """
        AppBox configuration for res_partner""",

    'description': """
        Android App: https://play.google.com/store/apps/details?id=com.odooappbox
        iPhone App: https://apps.apple.com/us/app/odooappbox/id1465496744
    """,

    'author': "You Zengjian",
    'website': "https://github.com/youzengjian/OdooAppBox",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'appbox'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/app_view_res_partner.xml',
        'data/app_action.xml',
        'data/app_menu.xml',
    ],
    'application': True,
}