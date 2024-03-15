# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Comparison Sheet',
    'version': '14.0.1.3',
    'sequence': 1,
    'category': 'Purchase',
    'description':
        """
        This Module add below functionality into odoo

        1.Compare price of different suppliers into excel sheet

    """,
    'summary': 'Comparison sheet',
    'author': 'BZ',
    'depends': ['purchase_requisition', 'Highland_purchase_indent'],
    'data': [
        'views/indent_views.xml',
        'views/purchase_order_view.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
