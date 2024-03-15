# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class ElectronicOrder(models.Model):
    _name = "electronic.order"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Electronic Order"

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self:_('New'))
    product_id = fields.Many2one('electronic.product', string='Company Name', required=True)
    price = fields.Integer(string='Price', related='product_id.price', tracking=True)
    item = fields.Selection([
        ('select', 'Select'),
        ('mobile', 'Mobile'),
        ('laptop', 'Laptop'),
        ('earphone', 'Ear Phone'),
        ('fan', 'Fan'),
        ('led', 'Led'),
    ], required=True, default='select', tracking=True)
    note = fields.Text(string='Description')
    date_order = fields.Date(string="Date")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Electronic Item'
        if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code('electronic.product') or _('New')
        res = super(ElectronicOrder, self).create(vals)
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            if self.product_id.item:
                self.item = self.product_id.item
            if self.product_id.note:
                self.note = self.product_id.note
        else:
            self.item = ''
            self.note = ''

