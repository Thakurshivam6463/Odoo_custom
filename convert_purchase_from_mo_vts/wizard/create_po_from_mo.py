import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class CreatePOFromMO(models.TransientModel):
    _name = 'create.po.from.mo'
    _description = "Create Purchase Order from Manufacturing"

    raw_material_line_ids = fields.One2many('manufacture.orderdata', 'raw_material_line_id',String="Raw Material")
    partner_id = fields.Many2one('res.partner', string='Vendor', required = True)
    date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)
    payment_term = fields.Many2one('account.payment.term',string='Payment Term')
    currency_id = fields.Many2one('res.currency',string='Currency',default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company',string='Company',default=lambda self: self.env.user.company_id)
    
    @api.model
    def default_get(self,  default_fields):
        res = super(CreatePOFromMO, self).default_get(default_fields)
        data = self.env['mrp.production'].browse(self._context.get('active_ids',[]))
        vals = []
        for record in data.move_raw_ids:
            vals.append((0,0,{
                            'product_id' : record.product_id.id,
                            'product_uom' : record.product_uom.id,
                            'name' : record.product_id.name,
                            'product_qty' : record.product_uom_qty,
                            'price_unit' : record.price_unit,
                            }))
        res.update({'raw_material_line_ids':vals})
        return res
    
    @api.multi
    def _prepare_purchase_order_line(self,po,order_line):
        purchase_order_line = self.env['purchase.order.line']
        product_qty = order_line.product_uom._compute_quantity(order_line.product_qty,order_line.product_id.uom_po_id)
        product_uom = order_line.product_id.uom_po_id.id
        price_unit = order_line.product_uom._compute_price(order_line.price_unit, order_line.product_id.uom_po_id)
        vals = {
            'product_id' : order_line.product_id.id,
            'name' : order_line.name,
            'order_id':po.id,
            'product_qty' : product_qty,
            'product_uom' : product_uom,
            'date_planned' : datetime.today(),
            'price_unit' : price_unit,
            'taxes_id':[(6,0,order_line.product_id.supplier_taxes_id.ids)]
        }
        line = purchase_order_line.create(vals)
    
    @api.multi
    def action_create_po_from_mo(self):
        self.ensure_one()
        purchase_order_obj = self.env['purchase.order']
        mrp_id = self.env['mrp.production'].browse(self._context.get('active_ids',[]))
        po = self.env['purchase.order'].search([('partner_id', '=',self.partner_id.id),('state', '=', 'draft'),('company_id', '=',mrp_id.company_id.id)],limit=1)
        if not po:
            vals = {
                'partner_id' : self.partner_id.id,
                'date_order' : self.date_order,
                'currency_id':self.currency_id.id,
                'payment_term_id':self.payment_term.id,
                'company_id':self.company_id.id,
                }
            po = purchase_order_obj.new(vals)
            po.onchange_partner_id()
            po_data = purchase_order_obj._convert_to_write({name:po[name] for name in po._cache})
            po_data.update({
                'partner_id' : self.partner_id.id,
                'date_order' : self.date_order,
                'payment_term_id':self.payment_term.id,
                'currency_id':self.currency_id.id or mrp_id.company_id.currency_id.id,
                'company_id':self.company_id.id
            })
            po = purchase_order_obj.with_context(company_id=self.company_id.id).create(po_data)
        for data in self.raw_material_line_ids:
            update = False
            for line in po.order_line:
                product_qty = data.product_uom._compute_quantity(data.product_qty,data.product_id.uom_po_id)
                product_uom = data.product_id.uom_po_id.id
                price_unit = data.product_uom._compute_price(data.price_unit, data.product_id.uom_po_id)
                if line.product_id.id == data.product_id.id and line.product_uom == data.product_id.uom_po_id:
                    vals = {
                        'product_uom':product_uom,
                        'product_qty':line.product_qty + product_qty,
                        'price_unit':price_unit
                        }
                    line.write(vals)
                    update = True
            if update == False:
                self._prepare_purchase_order_line(po,data)
        mrp_id.purchase_ids = [(4,po.id)]
        return po

class Manufactureorderdata(models.TransientModel):
    _name = 'manufacture.orderdata'
    _description = "Manufacturing Raw Material Data"

    raw_material_line_id = fields.Many2one('create.po.from.mo')

    product_id = fields.Many2one('product.product', string="Product", required=True)
    name = fields.Char(string="Description")
    product_qty = fields.Float(string='Quantity', required=True)
    date_planned = fields.Date(string='Scheduled Date', default = datetime.today())
    product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
    price_unit = fields.Float(string='Unit Price', required=True, digits=dp.get_precision('Product Price'))
    product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')

    @api.depends('product_qty', 'price_unit')
    def _compute_total(self):
        for record in self:
            record.product_subtotal = record.product_qty * record.price_unit
