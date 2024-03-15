from odoo import api, models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    logo_11 = fields.Binary(string='Logo 11')
    logo_12 = fields.Binary(string='Logo 12')