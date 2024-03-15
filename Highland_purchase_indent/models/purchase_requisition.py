# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class purchase_requisition_line(models.Model):
	_inherit = 'purchase.requisition.line'

	pi_number = fields.Char(string='Indent Number', default='005')

class purchase_requisition_line(models.Model):
	_inherit = 'purchase.requisition.line'

class purchase_requisition(models.Model):
	_inherit = 'purchase.requisition'

	def compute_count(self):
		for record in self:
			po_indent_ids = self.purchase_indent_ids and self.purchase_indent_ids.ids or 1
			if po_indent_ids:
				record.indent_count = len(str(po_indent_ids))

	purchase_indent_ids = fields.Many2many('purchase.indent', string='Purchase Indent', copy=False)
	indent_count = fields.Integer('Indent', compute='compute_count')
	
	def get_indent(self):
		"""Indent smart button"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Purchase Indent',
			'view_mode': 'tree,form',
			'res_model': 'purchase.indent',
			'domain': [('id', '=', self.purchase_indent_ids and self.purchase_indent_ids.ids or False)],
			'context': "{'create': False}"
		}



