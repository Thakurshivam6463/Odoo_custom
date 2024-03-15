{
    'name' : "Convert Purchase from Manufacture Order",
    'version' : "14.0.1",
    'license': 'OPL-1',
    'summary': 'This apps helps to Purchase Raw Material from Manufacturing Order',
    'category' : "Purchases",
    'depends'  : ['base','mrp','purchase'],
    'data'     : [
                'wizard/purchase_order_from_manufacturing.xml',
                'views/mrp_production.xml',
            ],
    'qweb': [
        ],
    'images': ['static/description/convert_po_from_mo.jpg'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
