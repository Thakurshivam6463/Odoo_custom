# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Sale Project',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Project',
    'description':
        """
        This Module add below functionality into odoo

        1.Sale Project

    """,
    'author': '',
    'summary': 'Project Sale',
    'depends': ['sale_management','sale_crm','project','sale_project','maintenance'],
    'data': [
            'security/ir.model.access.csv',
            'views/res_config_views.xml',
            #'views/crm_views.xml',
            'views/model_testing.xml',
            'views/testing_checklist.xml',
            'views/testing_location.xml',
            'views/sale_order_views.xml',
            'views/project_project_views.xml',
            'wizard/create_testing_views.xml',
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
