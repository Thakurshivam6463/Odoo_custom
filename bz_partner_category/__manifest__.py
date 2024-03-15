# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Bz Partner Category',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Purchase',
    'description':
        """
       Partner Category

    """,
    'summary': 'Partner Category',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.models.access.csv',
        'views/partner_category.xml',
        'views/partner.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
