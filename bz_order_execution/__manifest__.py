# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Bz Order Execution',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Bz Order Execution',
    'description':
        """
       Bz Order Execution

    """,
    'summary': 'Bz Order Execution',
    'depends': ['report_xlsx', 'production'],
    'data': [
            'security/ir.models.access.csv',
            'views/order_execution.xml',
            'report/report.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
