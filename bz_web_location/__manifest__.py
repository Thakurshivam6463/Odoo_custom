# -*- coding: utf-8 -*-

{
    'name': 'Location wise services',
    'description': 'Location wise services',
    'category': 'Concultancy',
    'summary': 'Location wise services',
    'version': '14.0',
    'license': 'AGPL-3',
    'sequence': -110,
    'website': 'https://www.bonzapro.com/',
    'depends': ['website', 'sale', 'product', 'theme_prime',],
    'data': [
        'security/ir.models.access.csv',
        'views/location_conf_view.xml',
        'views/location_inherit.xml',
        # 'views/template.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
}
