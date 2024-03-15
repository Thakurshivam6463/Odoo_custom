# -*- coding: utf-8 -*-
##############################################################################
{
    'name' : 'Fish Management',
    'category' : 'MRP',
    'sequence' : '-200',
    'description' : """Manage and Enhance the fishing business""",
    'depends' : ['stock', 'uom'],
    'data': [
        'security/ir.models.access.csv',
        'views/production.xml',
        'views/configration.xml',
        'views/value_add_product.xml',
        'views/start_time.xml',
        'views/soak_out_detail.xml',
        'views/load_unload.xml',
        'views/cold_store.xml',
        'views/freezer.xml',
    ],
    'qweb' : [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}