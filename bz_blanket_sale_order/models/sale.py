from odoo import models, fields

class saleOrder(models.Model):
    _inherit = "sale.order"

    bk_ref_id = fields.Integer('Blanket ID')

class saleOrderLine(models.Model):
    _inherit = "sale.order.line"

    bk_ref_id = fields.Integer('Blanket ID')

