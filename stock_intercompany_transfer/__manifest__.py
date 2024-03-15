# -*- coding: utf-8 -*-
###################################################################################

{
    'name': 'Inter Company Stock Transfer',
    'version': '14.0.1.0.0',
    'summary': """Create counterpart Receipt/Delivery Orders between companies.""",
    'description': """Automatically Create Receipt/Delivery orders if any company validates a 
                      Deliver Order/Receipt to the selected company,Inter Company Stock Transfer, Stock Transfer,
                      Create counterpart Receipt/Delivery Orders between companies""",
    'category': 'Warehouse',
    'depends': ['stock', 'account'],
    'data': [
        'views/res_company_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
