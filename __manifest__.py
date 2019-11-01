# -*- coding: utf-8 -*-
{
    'name': "Inceptus Base",

    'summary': """
        Base module for Inceptus Odoo addons""",

    'description': """
        Base module for Inceptus Odoo addons
    """,

    'author': "Inceptus.io",
    'website': "http://www.inceptus.io",

    'category': 'tools',
    'version': '13.0.0.1',

    'depends': ['base'],

    'data': [
        'data/ies_base_data.xml',
        'views/views.xml',
        'wizard/activation_wizard_view.xml',
    ],

    'installable': True,
    'auto_install': True,
    'application': False,
}
