# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Sale Dynamic Approval workflow',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
       This Module add below functionality into odoo

        1.Sale Dynamic Approval\n

    """,
    'summary': 'allow Sale Dynamic Approval by user/gropus',
    'depends': ['sale'],
    'data': [
        'security/ir.models.access.csv',
        'views/company_view.xml',
        'views/sale_view.xml'
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
