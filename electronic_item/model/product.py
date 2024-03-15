# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ElectronicProduct(models.Model):
    _name = "electronic.product"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Electronic Product"

    name = fields.Char(string='Company Name', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    price = fields.Integer(string='Price', tracking=True, required=True)
    item = fields.Selection([
        ('select', 'Select'),
        ('mobile', 'Mobile'),
        ('laptop', 'Laptop'),
        ('earphone', 'Ear Phone'),
        ('fan', 'Fan'),
        ('led', 'Led'),
    ], required=True, default='select', tracking=True)
    note = fields.Text(string='Description')
    image = fields.Binary(string="Patient Image")
    order_ids = fields.One2many('electronic.order', 'product_id', string='Orders')

    def compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Electronic Product'
        if vals.get('reference', _('New')) == _('New'):
           vals['reference'] = self.env['ir.sequence'].next_by_code('electronic.product') or _('New')
        res = super(ElectronicProduct, self).create(vals)
        return res

