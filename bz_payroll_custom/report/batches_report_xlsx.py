from odoo import models

class PayrollXlsx(models.AbstractModel):
    _name = 'report.bz_payroll_custom.report_batches_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Batches Report')
        bold = workbook.add_format({'bold': True})
        currency_format = workbook.add_format({'num_format': '$#,##0.00'})
        batch_account_details = self.env['batch.account.details'].search([], limit=1)
        sheet.set_column('C:G', 15)
        sheet.write(0, 2, 'Batches Report', bold)
        sheet.set_column('A:B', 15)
        active_id = data['context']['active_id']
        if active_id:
            payslip = self.env['hr.payslip.run'].browse(active_id)
            row = 2
            col = 0
            #Payslip Details
            sheet.write(row, col, 'Debit Customer ID', bold)
            if batch_account_details:
                sheet.write(row, col + 1, batch_account_details.debit_customer_id or '')
                sheet.write(row, col + 3, batch_account_details.serial_no or '')
                sheet.write(row + 1, col + 1, batch_account_details.debit_branch_id or '')
                sheet.write(row + 1, col + 3, batch_account_details.debit_account_no or '')
            sheet.write(row, col + 2, 'Serial No', bold)
            sheet.write(row + 1, col, 'Debit Branch ID', bold)
            sheet.write(row + 1, col + 2, 'Debit account Number', bold)

            sheet.write(row + 4, col, 'Payee ID', bold)
            sheet.write(row + 4, col + 1, 'Currency', bold)
            sheet.write(row + 4, col + 2, 'Payslip Ref', bold)
            sheet.write(row + 4, col + 3, 'Employee', bold)
            sheet.write(row + 4, col + 4, 'Designation', bold)
            sheet.write(row + 4, col + 5, 'Amount', bold)
            sheet.write(row + 4, col + 6, 'Particulars', bold)
            row = 7
            for payslip_val in payslip.slip_ids:
                net = 0.0
                for salary_line in payslip_val.line_ids:
                    if salary_line.category_id.name == 'Net':
                        net = salary_line.total
                emp_account_details = self.env['employees.accounts.details'].search([('employee_id', '=', payslip_val.employee_id.id)], limit=1)
                if emp_account_details:
                    payee_id = emp_account_details.payee_id
                else:
                    payee_id = ''
                sheet.write(row, col, payee_id)
                sheet.write(row, col + 1, 'INR')
                sheet.write(row, col + 2, payslip_val.number or '')
                sheet.write(row, col + 3, payslip_val.employee_id.name or '')
                sheet.write(row, col + 4, payslip_val.employee_id.job_title or '')
                sheet.write(row, col + 5, net or '')
                sheet.write(row, col + 6, str(payslip.date_start.strftime("%B")) + ' - ' + str(payslip.date_start.year) or '')
                row += 1
