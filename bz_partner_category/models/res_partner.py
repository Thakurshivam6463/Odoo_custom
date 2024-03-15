from odoo import models, api, _, fields

class PurchaseCategory(models.Model):
    _inherit = "res.partner"

    partner_category_id = fields.Many2one('partner.category', string='Category')