from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EmployeesAccountsDetails(models.Model):
    _name = "employees.accounts.details"
    _description = 'Employees Accounts Details'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    payee_id = fields.Char(string='Payee ID')
    account_number = fields.Char(string='Account Number')
    ifsc_code = fields.Char(string='IFSC code')

    @api.model
    def create(self, vals):
        if vals.get('employee_id'):
            record_available = self.search([('employee_id', '=', vals.get('employee_id'))])
            if record_available:
                raise ValidationError(_(
                    'Employee account details already created.'))
        res = super(EmployeesAccountsDetails, self).create(vals)
        return res

    def write(self, vals):
        res = super(EmployeesAccountsDetails, self).write(vals)
        if 'employee_id' in vals:
            record_available = self.search([('employee_id', '=', vals.get('employee_id'))])
            if record_available:
                raise ValidationError(_(
                    'Employee account details already created.'))
        return res


