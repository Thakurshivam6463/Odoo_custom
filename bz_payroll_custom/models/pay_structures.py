from odoo import models, fields, api, _

class PayStructures(models.Model):
    _name = "pay.structures"
    _description = 'Pay Structures'

    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company.id)
    currency_id = fields.Many2one("res.currency", string='Currency', related='company_id.currency_id',
                                  readonly=True)
    basic = fields.Monetary(string='Basic')
    hra = fields.Monetary(string='HRA')
    conveyance_allowance = fields.Monetary(string='Conveyance Allowance')
    food_allowance = fields.Monetary(string='Food Allowance')
    medical_allowance = fields.Monetary(string='Medical Allowance')
    special_allowance = fields.Monetary(string='Special Allowance')


