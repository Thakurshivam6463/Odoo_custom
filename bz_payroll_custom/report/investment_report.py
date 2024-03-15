# -- coding: utf-8 --
from odoo import models
import base64
import io

class InvestmentDeclarationXlsx(models.AbstractModel):
    _name = 'report.bz_payroll_custom.report_investment_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invs):
        sheet = workbook.add_worksheet('Investment')
        bold = workbook.add_format({'bold': True})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})

        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 25)
        sheet.set_column('F:F', 18)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)

        row = 1
        col = 1

        for personal in invs:
            sheet.write(row, col, 'Employee', bold)
            sheet.write(row, col + 1, personal.employee_id.name)
            sheet.write(row, col + 4, 'Date of Joining', bold)
            sheet.write(row, col + 5, personal.joining_date, date_style)
            row += 1
            sheet.write(row, col + 4, 'PAN', bold)
            sheet.write(row, col + 5, personal.employee_pan)
            row += 1
            sheet.write(row, col, 'Employee ID', bold)
            sheet.write(row, col + 1, personal.employee_identification)
            sheet.write(row, col + 4, 'Mobile', bold)
            sheet.write(row, col + 5, personal.mobile)

        row += 3

        sheet.merge_range(row, col, row, col + 7, 'HOUSE RENT DECLARATION', format_1)
        row += 1

        sheet.write(row, col, 'Landlord Name', bold)
        sheet.write(row, col+1, 'Street', bold)
        sheet.write(row, col+2, 'PAN', bold)
        sheet.write(row, col+3, 'Accommodation Address', bold)
        sheet.write(row, col+4, 'City', bold)
        sheet.write(row, col+5, 'Rent Payable', bold)
        sheet.write(row, col+6, 'Rent Effective From', bold)
        sheet.write(row, col+7, 'Rent Effective To', bold)

        object = data['context']['active_id']
        invest = self.env['investment.declaration'].browse(object)

        for line in invest.house_rent_line:
            row += 1
            sheet.write(row, col, line.landlord_name)
            sheet.write(row, col + 1, line.street)
            sheet.write(row, col + 2, line.pan)
            sheet.write(row, col + 3, line.accommodation_address)
            sheet.write(row, col + 4, line.city)
            sheet.write(row, col + 5, line.rent_Payable)
            sheet.write(row, col + 6, line.rent_effective_from, date_style)
            sheet.write(row, col + 7, line.rent_effective_to, date_style)


        row += 3
        sheet.merge_range(row, col, row, col + 7, 'INVESTMENT DECLARATION', format_1)
        row += 1

        sheet.write(row, col, 'Section', bold)
        sheet.write(row, col + 1, 'Expense', bold)
        sheet.write(row, col + 2, 'Description', bold)
        sheet.write(row, col + 3, 'Max Limit', bold)
        sheet.write(row, col + 4, 'Declared Amount', bold)

        # object = data['context']['active_id']
        # invest = self.env['investment.declaration'].browse(object)

        for obj in invest.investment_line:
            row += 1
            sheet.write(row, col, obj.section.section)
            sheet.write(row, col + 1, obj.expense.expense)
            sheet.write(row, col + 2, obj.description)
            sheet.write(row, col + 3, obj.max_limit)
            sheet.write(row, col + 4, obj.declared_amount)


