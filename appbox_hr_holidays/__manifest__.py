# -*- coding: utf-8 -*-
{
    'name': "appbox_hr_holidays",

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
    'depends': ['base', 'hr', 'hr_holidays', 'appbox', 'appbox_base', 'appbox_hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/app_view_hr_employee.xml',
        'data/app_view_hr_leave.xml',
        'data/app_action.xml',
    ],
    'application': True,
}