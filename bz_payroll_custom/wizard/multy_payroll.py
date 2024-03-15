from odoo import models, fields, api, _, tools
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
import babel

class MultyPayslipWizard(models.TransientModel):
    _name = "multi.payslip.wizard"
    _description = "Multi Payslip Wizard"

    employee_ids = fields.Many2many(
        'hr.employee', 'multi_payslip_rel', 'multi_payslip_id', 'employee_id', string='Employee', required=1)
    date_start = fields.Date(string='Date From', required=True,
                             default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_end = fields.Date(string='Date To', required=True,
                           default=lambda self: fields.Date.to_string(
                               (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    journal_id = fields.Many2one('account.journal', string='Salary Journal', required=True)

    @api.onchange('date_start', 'date_end')
    def onchange_period(self):
        employee_ids = self.env['hr.employee'].search([('active', '=', True)])
        if employee_ids:
            self.employee_ids = [(6, 0, employee_ids.ids)]

    def multi_payroll_create(self):
        for employee in self.employee_ids:
            contract = self.env['hr.contract'].search([('employee_id', '=', employee.id),('state', '=', 'open')])
            if contract:
                locale = self.env.context.get('lang') or 'en_US'
                ttyme = datetime.combine(fields.Date.from_string(self.date_start), time.min)
                vals = {
                    'employee_id': employee.id,
                    'date_from': self.date_start,
                    'date_to': self.date_end,
                    'struct_id': contract.struct_id.id,
                    'name': _('Salary Slip of %s for %s') % (
                        employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale))),
                    'journal_id': self.journal_id.id,
                    'contract_id': contract.id
                }
                payslip = self.env['hr.payslip'].create(vals)
                slip_data = payslip.onchange_employee_id(self.date_start, self.date_end, employee.id, contract_id=False)
                payslip.worked_days_line_ids = [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')]
                payslip.compute_sheet()








