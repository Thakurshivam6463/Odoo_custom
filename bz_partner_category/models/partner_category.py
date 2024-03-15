from odoo import models, api, _, fields

class PurchaseCategory(models.Model):
    _name = "partner.category"

    name = fields.Char('Name')
    code = fields.Char('Code')



