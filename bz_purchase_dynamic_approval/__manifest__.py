# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Purchase Dynamic Approval workflow',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Purchase',
    'description':
        """
       This Module add below functionality into odoo

        1.Purchase Dynamic Approval\n

    """,
    'summary': 'allow Purchase Dynamic Approval by user/gropus',
    'depends': ['purchase'],
    'data': [
        'security/ir.models.access.csv',
        'security/purchase_security.xml',
        'views/company_view.xml',
        'views/purchase_view.xml'
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
