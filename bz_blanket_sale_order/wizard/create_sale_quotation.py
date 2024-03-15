from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class CreateSaleQuotation(models.TransientModel):
    _name = "create.sale.quotation"
    _description = "Create Sale Quotation"

    name = fields.Char('Name')
    bk_ref_id = fields.Integer('Blanket ID')
    quotation_line_ids = fields.One2many('blanket.quotation.line', 'ref_quotation_id', string='Reference', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', change_default=True, index=True, tracking=1)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')
    user_id = fields.Many2one('res.users', string='Salesperson')


    def blanket_quotation_create(self):
        partner_id = False
        if self.partner_id:
            partner_id = self.partner_id
        if self.quotation_line_ids:
            new_quotation = self.env['sale.order'].create({'partner_id': partner_id.id, 'origin': self.name})
            for req in self.quotation_line_ids:
                if req.new_quotation_qty > req.remaining_qty:
                    raise ValidationError(_('New Quotation Quantity could not be grater than Remaining Quantity.'))
                if req.new_quotation_qty ==  0.0:
                    raise ValidationError(_('New Quotation Quantity is empty.'))
                new_quotation.write({'bk_ref_id': self.bk_ref_id,
                                     'user_id': self.user_id.id,
                                     'payment_term_id': self.payment_term_id.id,
                                     'order_line': [(0, 0, {'product_id': req.product_id.id,
                                                            'product_uom_qty': req.new_quotation_qty,
                                                            'tax_id': [(6, 0, req.tax_id.ids)],
                                                            'bk_ref_id': self.bk_ref_id,
                                                            })]
                                  })

                blanket_obj = self.env['so.blanket.line'].search([('product_id', '=', req.product_id.id),('order_id', '=', self.bk_ref_id)])
                if blanket_obj:
                    blanket_obj.remaining_qty = req.remaining_qty - req.new_quotation_qty
                    # blanket_obj.


class BlanketQuotationLine(models.TransientModel):
    _name = "blanket.quotation.line"
    _description = "Blanket Quotation Line"

    partner_id = fields.Many2one(
        'res.partner', string='Customer', required=True, change_default=True, readonly=True)
    product_id = fields.Many2one('product.product', string='Product', domain="[('sale_ok', '=', True)]", readonly=True)
    remaining_qty = fields.Float(string='Remaining Quantity', digits='Product Unit of Measure', readonly=True)
    new_quotation_qty = fields.Float(string='New Quotation Quantity', digits='Product Unit of Measure', required=True)
    ref_quotation_id = fields.Many2one('create.sale.quotation', string='Reference')
    tax_id = fields.Many2many('account.tax', string='Taxes', context={'active_test': False,}, readonly=True)
    bk_ref_id = fields.Integer('Blanket ID')

    @api.onchange('new_quotation_qty')
    def _onchange_new_quotation_qty(self):
        if self.new_quotation_qty > self.remaining_qty:
            raise ValidationError(_('New Quotation Quantity could not be grater than Remaining Quantity.'))






