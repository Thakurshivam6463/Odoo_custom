# -*- coding: utf-8 -*-
##############################################################################
{
    'name' : 'Fish Management',
    'category' : 'MRP',
    'description' : """Manage and Enhance the fishing business""",
    'depends' : ['mrp', 'sale', 'account', 'stock', 'fleet', 'uom'],
    'data': [
        'security/ir.models.access.csv',
        'data/sequence.xml',
        'views/gate_entry_view.xml',
        'views/materials_reciving_deck_views.xml',
        'views/planning_view.xml',
        'views/qc_view.xml',
        'views/processing_view.xml',
        'views/reprocessing_view.xml',
        'views/batch_view.xml',
        'views/grade_operation_views.xml',
    ],
    'qweb' : [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}