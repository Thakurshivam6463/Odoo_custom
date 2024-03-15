from odoo import models, fields, api, _, tools

class MultyPayslipConfirmWizard(models.TransientModel):
    _name = "multi.payslip.confirm.wizard"
    _description = "Multi Payslip Confirm Wizard"

    payroll_ids = fields.Many2many(
        'hr.payslip', 'multi_payroll_confirm_rel', 'multi_payroll_confirm_id', 'payroll_id', string='Payrolls', required=1,
        default=lambda self: self.env['hr.payslip'].search([('state', 'not in', ['done', 'cancel'])]).ids
        )

    def multi_payroll_confirm(self):
        for payslip in self.payroll_ids:
            payslip.action_payslip_done()
