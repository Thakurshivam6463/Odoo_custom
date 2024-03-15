# -*- coding: utf-8 -*-
{
    'name': "Purchase Dashboard",
    'version': '14.0.1.0.3',
    'summary': """Purchase Dashboard""",
    'description': """Purchase Dashboard""",
    'category': 'Purchase',
    'depends': ['base', 'purchase', 'purchase_requisition','hr'],
    'data': [
        'security/ir.models.access.csv',
        'views/purchase_dashboard.xml',
        'views/purchase_requisition.xml',
    ],
    'qweb': ["static/src/xml/dashboard.xml"],
    'license': "AGPL-3",
    'installable': True,
    'application': True,
}
