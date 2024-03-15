# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class CreateOrderWizard(models.TransientModel):
    _name = "create.order.wizard"
    _description = "Create Order Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CreateOrderWizard, self).default_get(fields)
        res['product_id'] = self._context.get('active_id')
        return res

    product_id = fields.Many2one('electronic.product', string="Product", required=True)
    date_order = fields.Date(string='Date', required=False)

    def action_create_order(self):
        vals = {
            'product_id': self.product_id.id,
            'date_order': self.date_order
        }
        order_rec = self.env['electronic.order'].create(vals)
        return {
            'name': _('Order'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'electronic.order',
            'res_id': order_rec.id,
            'target': 'new',
        }

    def action_view_order(self):
        action = self.env.ref('electronic_item.action_electronic_order').read()[0]
        action['domain'] = [('product_id', '=', self.product_id.id)]
        return action