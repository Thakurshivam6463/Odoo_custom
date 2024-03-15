from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    joining_date = fields.Date(string='Date of Joining')
    pan = fields.Char(string='PAN')
    aadhar = fields.Char(string='Aadhar')
    mobile = fields.Char(string='Mobile')
    pf_account = fields.Char(string='PF Account')
    unique_employee_id = fields.Char(string='Employee ID')

    @api.model
    def create(self, vals):
        vals['unique_employee_id'] = self.env['ir.sequence'].next_by_code('hr.employee')
        res = super(HrEmployee, self).create(vals)
        return res

