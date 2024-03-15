# -*- coding: utf-8 -*-
{
    'name': 'incoming',
    'version': '1.0',
    'summary': 'incoming',
    'sequence': -100,
    'description': """TRF""",
    'category': 'Testing',
    'website': 'https://www.bonzapro.com',
    'depends': ['crm', 'mail', 'sale', 'project', 'maintenance'],
    'data': [
        'views/incoming_views.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
