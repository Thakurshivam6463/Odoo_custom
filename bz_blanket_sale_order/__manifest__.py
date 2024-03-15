# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Blanket Sale Order workflow',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Sale',
    'description':
        """
       Blanket Sale Order workflow

    """,
    'summary': 'Blanket Sale Order workflow',
    'depends': ['sale'],
    'data': [
        'security/ir.models.access.csv',
        'security/blanket_order_group.xml',
        'data/ir_sequence_data.xml',
        'data/service_cron.xml',
        'views/so_blanket_views.xml',
        'wizard/create_sale_quotation_view.xml',
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
