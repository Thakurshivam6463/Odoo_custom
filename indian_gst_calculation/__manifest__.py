# -*- coding: utf-8 -*-
{
    'name': "GST Invoice (India)",

    'summary': 
        """
        GST Invoice (India) is develped to implement the GST launched on 1st July, 2017.
        """,
    'license': 'OPL-1',

    'description': """
        - This module has categorised the taxes as per new GST.
        
        - CGST, SGST, IGST and UTGST categories speicfies tax revenue.

        - Product tax percentage is shared on GST type selected by user. 
          for e.g. if CGST + SGST type is selected, product tax precentage is shared between CGST and SGST and relavent amount
          is displayed infCGST and SGST columns respectively.

        - Sale Order and Invoice forms are configured with these GST categories.
    """,
    'price': 10.00,
    'currency': 'EUR',
    'author': "Techspawn Solutions",
    'website': "http://www.techspawn.com",
    'images': ['static/description/main.jpg'],
    'category': 'Accounting and Tax',
    'version': '0.1',

    'depends': ['base', 'sale', 'purchase', 'account', 'sales_team','sale_management', 'stock','kuodoo_extended'],

    'data': [
        'security/ir.models.access.csv',
        'views/account_invoice.xml',
        'views/account_invoice_report.xml',
        'views/account_tax.xml',
        'views/product_hsn_settings.xml',
        'views/product_template.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/res_company.xml',
        'views/sale_order_report.xml',
        'views/purchase_order.xml',
        'views/purchase_order_report.xml',
        'views/purchase_request_report.xml',
    ],

}
