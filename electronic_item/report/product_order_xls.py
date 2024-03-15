# -*- coding: utf-8 -*-
from odoo import models
import base64
import io

class ProductOrderXlsx(models.AbstractModel):
    _name = 'report.electronic_item.report_order_details_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, product):
        sheet = workbook.add_worksheet('Orders')
        bold = workbook.add_format({'bold': True})

        sheet.set_column('D:D', 10)
        sheet.set_column('E:E', 23)

        row = 3
        col = 3

        sheet.write(row, col, 'Reference', bold)
        sheet.write(row, col + 1, 'Product Name', bold)

        for order in data['orders']:
            row += 1
            sheet.write(row, col, order['name'])
            sheet.write(row, col + 1, order['product_id'][1])