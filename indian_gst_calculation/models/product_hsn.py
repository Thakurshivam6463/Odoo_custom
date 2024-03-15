# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomProducts(models.Model):
	_name = 'custom.products'

	name = fields.Char(string="Product")
	custom_product_type = fields.Selection(selection=[('goods', 'Goods'),
												('services', 'Services')], 
												string="Type")
	HSN_SAC = fields.Char(string="HSN/SAC Code")
	appl_tax = fields.Many2one('account.tax',string="GST Rate")