from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    modification_end_date = fields.Date(string='Modification End Date')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('bz_payroll_custom.modification_end_date', self.modification_end_date)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        modification_end_date = ICPSudo.get_param('bz_payroll_custom.modification_end_date')
        res.update(
            modification_end_date=modification_end_date
        )
        return res

    @api.onchange('modification_end_date')
    def _onchange_modification_end_date(self):
        if self.modification_end_date:
            employee_ids = self.env['hr.employee'].search([])
            if employee_ids:
                ICPSudo = self.env['ir.config_parameter'].sudo()
                modification_end_date = ICPSudo.get_param('bz_payroll_custom.modification_end_date')
                for employee in employee_ids:
                    investment = self.env['investment.declaration'].search([('employee_id', '=', employee.id)], limit=1)
                    if investment:
                        investment.modification_end_date = modification_end_date

