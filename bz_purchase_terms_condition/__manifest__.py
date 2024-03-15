{
    'name': 'Purchase Terms and Conditions',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Purchase Terms and Condition',
    'description':
        """
        This Module add below functionality into odoo

        1.Purchase Terms and Condition\n

    """,
    'summary': 'Purchase Terms and Condition',
    'author': '',
    'website': '',
    'depends': ['purchase'],
    'data': [
        'security/ir.models.access.csv',
        'views/term_condition_view.xml',
        'views/purchase_view.xml',
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