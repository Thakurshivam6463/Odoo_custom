from odoo import models
from datetime import date, datetime

class PayrollXlsx(models.AbstractModel):
    _name = 'report.bz_payroll_custom.report_payroll_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('PaySlip Report')
        bold = workbook.add_format({'bold': True})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
        sheet.set_column('C:E', 20)
        sheet.write(0, 2, 'PaySlip Report', bold)
        sheet.set_column('A:B', 20)
        active_id = data['context']['active_id']
        if active_id:
            payslip = self.env['hr.payslip'].browse(active_id)
            row = 2
            col = 0
            #Employee Details
            sheet.write(row, col, 'Name', bold)
            sheet.write(row, col + 1, payslip.employee_id.name)
            sheet.write(row, col + 2, 'Designation', bold)
            sheet.write(row, col + 3, payslip.employee_id.job_title)
            sheet.write(row + 1, col, 'Address', bold)
            sheet.write(row + 1, col + 1, payslip.employee_id.address_home_id.name or '')
            sheet.write(row + 2, col + 1, payslip.employee_id.address_home_id.street or '')
            sheet.write(row + 3, col + 1, payslip.employee_id.address_home_id.street2 or '')
            sheet.write(row + 4, col + 1, payslip.employee_id.address_home_id.city or '')
            sheet.write(row + 5, col + 1, payslip.employee_id.address_home_id.state_id.name or '')
            sheet.write(row + 6, col + 1, payslip.employee_id.address_home_id.zip or '')
            sheet.write(row + 7, col + 1, payslip.employee_id.address_home_id.country_id.name or '')
            sheet.write(row + 8, col + 1, payslip.employee_id.address_home_id.phone or '')
            sheet.write(row + 9, col, 'Email', bold)
            sheet.write(row + 9, col + 1, payslip.employee_id.private_email or '')
            sheet.write(row + 9, col + 2, 'Identification No', bold)
            sheet.write(row + 9, col + 3, payslip.employee_id.identification_id or '')
            sheet.write(row + 10, col, 'Reference', bold)
            sheet.write(row + 10, col + 1, payslip.number or '')
            sheet.write(row + 10, col + 2, 'Bank Account', bold)
            # sheet.write(row + 10, col + 3, payslip.employee_id.bank_account_id.name or '')
            sheet.write(row + 11, col, 'Date From', bold)
            sheet.write(row + 11, col + 1, payslip.date_from or '', date_style)
            sheet.write(row + 11, col + 2, 'Date To', bold)
            sheet.write(row + 11, col + 3, payslip.date_to or '', date_style)
            sheet.write(row + 12, col, 'Aadhar', bold)
            sheet.write(row + 12, col + 1, payslip.employee_id.aadhar or '')
            sheet.write(row + 12, col + 2, 'PAN', bold)
            sheet.write(row + 12, col + 3, payslip.employee_id.pan or '')
            #Allowance
            sheet.write(row + 14, col, 'Income', bold)
            sheet.write(row + 14, col + 1, 'For the Month Rs.', bold)
            sheet.write(row + 15, col, 'Basic')
            sheet.write(row + 15, col + 1, payslip.basic or '')
            sheet.write(row + 16, col, 'HRA')
            sheet.write(row + 16, col + 1, payslip.hra_exemption or '')
            sheet.write(row + 17, col, 'Conveyance Allowance')
            sheet.write(row + 17, col + 1, payslip.conveyance_allowance or '')
            sheet.write(row + 18, col, 'Food Allowance')
            sheet.write(row + 18, col + 1, payslip.food_allowance or '')
            sheet.write(row + 19, col, 'Medical Allowance')
            sheet.write(row + 19, col + 1, payslip.medical_allowance or '')
            sheet.write(row + 20, col, 'Special Allowance')
            sheet.write(row + 20, col + 1, payslip.special_allowance or '')
            sheet.write(row + 21, col, 'Gross Salary', bold)
            sheet.write(row + 21, col + 1, payslip.basic + payslip.hra_exemption + payslip.conveyance_allowance +
                        payslip.medical_allowance + payslip.special_allowance + payslip.food_allowance, bold)
            #Deduction
            sheet.write(row + 14, col + 2, 'Deductions', bold)
            sheet.write(row + 14, col + 3, 'For the Month Rs.', bold)
            row = 17
            total_deduction = 0.0
            for investment in payslip.investment_line:
                sheet.write(row , col + 2, investment.expense.expense)
                sheet.write(row, col + 3, round((investment.declared_amount)/12, 2))
                total_deduction += (investment.declared_amount)/12
                row += 1
            sheet.write(row, col + 2, 'Total Deduction', bold)
            sheet.write(row, col + 3, round(total_deduction, 2), bold)
            sheet.write(row + 1, col + 2, 'Net Pay', bold)
            sheet.write(row + 1, col + 3, round((payslip.basic + payslip.hra_exemption + payslip.conveyance_allowance +
                        payslip.medical_allowance + payslip.special_allowance + payslip.food_allowance)
                                                - total_deduction, 2), bold)
