# -*- coding: utf-8 -*-
{
    'name' : 'Electronic Shop',
    'version' : '1.1',
    'summary': 'Electronic Shop Software',
    'sequence': -100,
    'description': """The electronics industry has taken a stride over the market with the huge demand for electronics goods.""",
    'category': 'Productivity',
    'website': 'https://www.odoomates.tech',
    'depends': ['mail',
                'report_xlsx'],
    'data': [
        'security/ir.models.access.csv',
        'wizard/create_order_view.xml',
        'wizard/order_report_view.xml',
        'view/product.xml',
        'view/my_module_data.xml',
        'view/laptop.xml',
        'view/order.xml',
        'report/product_details_template.xml',
        'report/order_details.xml',
        'report/report.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
