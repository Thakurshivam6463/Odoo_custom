from odoo import fields, models


class PurchaseTermCondition(models.Model):
    _name = 'purchase.term.condition'
    
    name = fields.Char(string='Name')
    terms = fields.Text(string='Terms')