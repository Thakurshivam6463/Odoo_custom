# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Bz Purchase Requisition',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Purchase',
    'description':
        """
       Purchase Requisition

    """,
    'summary': 'Purchase Requisition',
    'depends': ['purchase_requisition'],
    'data': [
        'views/purchase_requisition_view.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
