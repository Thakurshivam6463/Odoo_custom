from odoo import models, fields, api, _

class HrContract(models.Model):
    _inherit = "hr.contract"

    wage = fields.Monetary('Basic', required=False, tracking=True, help="Employee's monthly gross wage.")
    meal_allowance = fields.Monetary(string="Food Allowance", help="Food allowance")
    other_allowance = fields.Monetary(string="Special Allowance", help="Special allowances")
    pf = fields.Char(string="PF", help="Provident Fund")
    pt = fields.Monetary(string="PT", help="Professional Tax")
    tds = fields.Monetary(string="TDS", help="Tax Deducted at Source")
    conveyance_allowance = fields.Monetary(string="Conveyance Allowance", help="conveyance_allowance")
    is_type_id = fields.Boolean(string="Is Employee Category")
    consultant_pay = fields.Monetary(string="Professional Charges")
    consultant_tds = fields.Char(string='Consultant TDS')
    hra_exemptions = fields.Float(string='HRA Exemptions')
    pay_structure = fields.Many2one('pay.structures', string='Pay Structure')
    # standard_deduction = fields.Monetary('Standard Deduction')


    @api.onchange('type_id')
    def _onchange_type_id(self):
        if self.type_id.name == 'Consultant':
            self.is_type_id = True
        else:
            self.is_type_id = False

    @api.onchange('pay_structure')
    def _onchange_pay_structure(self):
        if self.pay_structure:
            self.wage = self.pay_structure.basic
            self.hra = self.pay_structure.hra
            self.conveyance_allowance = self.pay_structure.conveyance_allowance
            self.meal_allowance = self.pay_structure.food_allowance
            self.medical_allowance = self.pay_structure.medical_allowance
            self.other_allowance = self.pay_structure.special_allowance

