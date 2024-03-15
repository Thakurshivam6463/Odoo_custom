# -*- coding: utf-8 -*-
from odoo import models
import base64
import io

class ProductXlsx(models.AbstractModel):
    _name = 'report.electronic_item.report_product_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, products):
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        sheet = workbook.add_worksheet('Product')
        row = 3
        col = 3
        sheet.set_column('D:D', 15)
        sheet.set_column('E:E', 13)

        for obj in products:
            row += 1
            sheet.merge_range(row, col, row, col + 1, 'Product', format_1)

            if obj.image:
                patient_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row+1, col, "image.png", {'image_data': patient_image, 'x_scale': 0.5, 'y_scale': 0.5})

                row += 6

            row += 1
            sheet.write(row, col, 'Reference', bold)
            sheet.write(row, col + 1, obj.reference)
            row += 1
            sheet.write(row, col, 'Company Name', bold)
            sheet.write(row, col + 1, obj.name)
            row += 1
            sheet.write(row, col, 'Price', bold)
            sheet.write(row, col + 1, obj.price)
            row += 1
            sheet.write(row, col, 'Item', bold)
            sheet.write(row, col + 1, obj.item)
            row += 2