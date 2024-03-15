import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    @api.depends('purchase_ids')
    def _compute_purchase_order(self):
        for order in self:
            order.purchase_count = len(order.purchase_ids)
            
    purchase_count = fields.Integer(compute="_compute_purchase_order", string='# of Order', copy=False, default=0, store=True)
    purchase_ids = fields.Many2many('purchase.order',string="Purchase Order")
    
    # @api.multi
    # def action_view_purchase_order(self):
    #     action = self.env.ref('purchase.purchase_rfq')
    #     result = action.read()[0]
    #
    #     result['context'] = {}
    #     purchase_order_ids = self.mapped('purchase_ids')
    #
    #     if len(purchase_order_ids) > 1:
    #         result['domain'] = "[('id','in',%s)]" % (purchase_order_ids.ids)
    #     elif len(purchase_order_ids) == 1:
    #         res = self.env.ref('purchase.purchase_order_form', False)
    #         result['views'] = [(res and res.id or False, 'form')]
    #         result['res_id'] = purchase_order_ids.id
    #     return result
