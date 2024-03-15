from odoo import models, api, _, fields

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    department = fields.Many2one('hr.department', string='Department')

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition.line"

    cost_center = fields.Char('Cost Center')
