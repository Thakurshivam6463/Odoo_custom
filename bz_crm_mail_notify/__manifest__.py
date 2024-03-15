# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Bz CRM Mail Notify',
    'version': '14.0.1.0',
    'sequence': 1,
    'description':
        """
       Bz CRM Mail Notify

    """,
    'summary': 'Bz CRM Mail Notify',
    'depends': ['crm', 'website_hr_recruitment'],
    'data': [
        'data/mail_template.xml',
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
