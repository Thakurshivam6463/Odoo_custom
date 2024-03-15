# -*- coding: utf-8 -*-
{
    'name' : 'Colege ERP',
    'version' : '14.0',
    'summary': 'College Management Software',
    'sequence': -100,
    'description': """College Management Software""",

    'category': 'Productivity',
    'website': 'https://www.odoomates.tech',
    'depends' : ['mail'],
    'data': [
        'security/ir.models.access.csv',
        'view/student.xml',
        'view/my_module_data.xml'
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
