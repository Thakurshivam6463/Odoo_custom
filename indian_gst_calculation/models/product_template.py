# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomProductTemplate(models.Model):
	"""
		Adds three HSN/SAC columns to product template models.
	"""
	_inherit = "product.template"

	custom_product_name = fields.Many2one('custom.products', string="Product")
	custom_product_type = fields.Selection(selection=[('goods', 'Goods'),
												('services', 'Services')], string="Type")
	HSN_SAC = fields.Char(string="HSN/SAC")

	@api.onchange('custom_product_name')
	def _get_hsn_code(self):
		self.HSN_SAC = ""
		self.HSN_SAC = self.custom_product_name.HSN_SAC

	@api.onchange('custom_product_type')
	def _get_products(self):
		self.custom_product_name = ""


class CustomProductProduct(models.Model):
	_inherit = "product.product"

	@api.onchange('custom_product_name')
	def _get_hsn_code(self):
		self.HSN_SAC = ""
		self.HSN_SAC = self.custom_product_name.HSN_SAC

	@api.onchange('custom_product_type')
	def _get_products(self):
		self.custom_product_name = ""
