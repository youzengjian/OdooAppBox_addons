# -*- coding: utf-8 -*-
{
    'name': "appbox core module",

    'summary': """
        Core module for android client and iPhone client""",

    'description': """
        Android App: https://play.google.com/store/apps/details?id=com.odooappbox
        iPhone App: https://apps.apple.com/us/app/odooappbox/id1465496744
    """,

    'author': "You Zengjian",
    'website': "https://github.com/youzengjian/OdooAppBox",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/actions.xml',
        'security/menus.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/app_menu.xml',
        'views/app_config.xml',
        'views/app_view.xml',
        'data/app_config.xml',
        'data/ir_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}