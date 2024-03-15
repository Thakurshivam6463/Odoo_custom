# -*- coding: utf-8 -*-

{
    'name': 'Multiple Invoice Payment',
    'category': 'Accounting',
    'summary': 'Multiple Invoice Payment',
    'version': '1.0',
    'description': """Multiple Invoice Payment""",
    'website': "https://apps.odoo.com/apps/",
    'license': "OPL-1",
    'price': "20",
    'currency': 'EUR',
    'depends': ['account'],
    'data': [
        'security/ir.models.access.csv',
        'views/account_payment_view.xml'
    ],
    'installable': True,
    'auto_install': True,
}
