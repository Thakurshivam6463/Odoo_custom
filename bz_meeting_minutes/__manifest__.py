# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'BZ Meeting Minutes',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Sale',
    'description':
        """
       Meeting of Minutes.

    """,
    'summary': 'Meeting of Minutes.',
    'depends': ['calendar'],
    'data': [
        'views/calendar.xml',
        'report/report.xml',
        'report/meeting_minute_layout.xml',
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
