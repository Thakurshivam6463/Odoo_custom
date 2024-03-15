# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Sale Meeting',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Sale',
    'description':
        """
       Create meeting for Sale Order.

    """,
    'summary': 'Create meeting for Sale Order.',
    'depends': ['sale', 'calendar'],
    'data': [
        'views/sale.xml',
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
