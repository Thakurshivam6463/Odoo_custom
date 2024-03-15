# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import AccessError, UserError, ValidationError

class AccountCostCenter(models.Model):
	_name = 'account.cost.center'

	name = fields.Char(string='Name')


class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'




#	indent_id = fields.Many2many('purchase.indent', string='Purchase Indent')
#	indent_count = fields.Integer('Indent',compute='compute_count')
	# cost_center = fields.Char('Cost Center')
	cost_center_id = fields.Many2one('account.cost.center', string='Cost Center')


	def button_confirm(self):
		purchase_obj = self.env['purchase.order'].search([('indent_id', '=', self.indent_id.id),
														('id', '!=', self.id)])
		for purchase in purchase_obj:
			purchase.state = 'cancel'
			purchase.cancel_remarks = 'Auto cancelled due to other RFQ is confimed.'
		super(PurchaseOrder, self).button_confirm()



class Picking(models.Model):
	_inherit = 'stock.picking'


	def compute_count(self):
		for record in self:
			record.indent_count = self.env['purchase.indent'].search_count([('picking_id', '=', self.id)])


	indent_id = fields.Many2one('purchase.indent', string='Purchase Indent')
	indent_count = fields.Integer('Indent',compute='compute_count')

	def get_indent(self):
		"""Indent smart button"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Indent',
			'view_mode': 'tree,form',
			'res_model': 'purchase.indent',
			'domain': [('picking_id', '=', self.id)],
			'context': "{'create': False}"
		}


class PurchaseIndent(models.Model):
	_name = 'purchase.indent'
	_inherit = ['mail.thread']
	_description = "Purchase Indent"
	_order = "id desc"

	def compute_count(self):
		for record in self:
			record.purchase_tender_count = len(self.purchase_requisition_ids and self.purchase_requisition_ids.ids)
			record.picking_count = self.env['stock.picking'].search_count([('indent_id', '=', self.id)])


	name = fields.Char(string='Indent No', default='New')
	indent_date = fields.Date(string='Indent date', readonly=True, default=datetime.today())
	employee_id = fields.Many2one('hr.employee', string='User', required=True,
									track_visibility='onchange')
	department_id = fields.Many2one('hr.department', string='Department', 
									track_visibility='onchange')
	purchase_tender_count = fields.Integer('Purchase Tender',compute='compute_count')
	purchase_requisition_ids = fields.Many2many('purchase.requisition',string="purchase Requisition",copy=False)
	picking_count = fields.Integer('Transfer',compute='compute_count')
	purchase_id = fields.Many2one('purchase.order', string='Purchase Indent')
	picking_id = fields.Many2one('stock.picking', string='Picking')
	state = fields.Selection([
		('new', 'New'),
		('department_validate', 'HOD Validated'),
		('approve', 'Waiting for Delivery'),
		('delivered', 'Delivered'),
		('partial', 'Partially-Delievered'),
		('in_progress', 'Waiting for HOD Approval'),
		('store_manager', 'Store Manager Validated'),
		('account', 'Accountant Validated'),
		('md_validated', 'MD Validated'),
		('rejected', 'Rejected'),
		('close', 'Closed'),
		], string='Status', readonly=True, copy=False, index=True, track_visibility='always', default='new')
	indent_type = fields.Selection([
		('normal', 'Normal'),
		('emergency', 'Emergency'),
		], string='Indent Type',track_visibility='always', default='normal')
	prod_ids = fields.One2many('product.details', 'prod_id', string='Product Details')
	reason = fields.Text(string='Reason for Indent', track_visibility='always')
	rejected_remarks = fields.Text(string='Rejected Remarks',track_visibility='always', readonly=True)
	rejected_user = fields.Many2one('res.users','Cancelled User', readonly=True)
	requestion_validater_id = fields.Many2one('hr.employee', string='HOD')
	store_manager_id = fields.Many2one('res.users',string="Store Manager")
	account_user_id = fields.Many2one('res.users',string="Account Manager")
	purchase_user_id = fields.Many2one('res.users',string="Purchaser")
	requestion_md_id = fields.Many2one('hr.employee', string='MD')
	material_required_date = fields.Date(string='Material required date')
	# cost_center = fields.Char('Cost Center')
	cost_center_id = fields.Many2one('account.cost.center', string='Cost Center')
	department_flag = fields.Boolean(string='Department Flag',copy=False , compute='get_department_flag')
	store_manager_flag = fields.Boolean(string='Store Manager',copy=False , compute='get_store_manager_flag')
	account_manager_flag = fields.Boolean(string='Account Manager Flag',copy=False , compute='get_account_manager_flag')
	md_flag = fields.Boolean(string='MD Flag',copy=False , compute='get_md_flag')
	purchase_user_flag = fields.Boolean(string='Purchase User Flag',copy=False , compute='get_po_flag')
	user_remarks = fields.Text('User Remarks',track_visibility='always')
	hod_remarks = fields.Text('HOD Remarks',track_visibility='always')
	sm_remarks = fields.Text('Store Manager Remarks',track_visibility='always')
	am_remarks = fields.Text('Accounts Manager Remarks',track_visibility='always')
	md_remarks = fields.Text('MD Remarks',track_visibility='always')
	purchaser_remarks = fields.Text('Purchaser Remarks',track_visibility='always')
	delivery_location = fields.Char('Delivery Location',track_visibility='always')
	company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
	
	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('purchase.indent')
		return super(PurchaseIndent, self).create(vals)

	@api.onchange('employee_id')
	def onchange_employee_id(self):
		if self.employee_id:
			self.department_id = self.employee_id.department_id.id

	@api.onchange('indent_type')
	def onchange_indent_type(self):
		self.indent_date = datetime.today()

	def submit_md_validate(self):
		if self.purchase_user_id and self.purchase_user_id.employee_id and self.purchase_user_id.employee_id.work_email:
			self.requestion_approval_send_mail(self.purchase_user_id.employee_id.work_email)
		self.state = 'md_validated'
		return True

	def button_close(self):
		self.state = 'close'

	def make_url(self):
		record_id = self.id
		menu_id = self.env.ref('Highland_purchase_indent.sub_menu_purchase_indent').id
		action_id = self.env.ref('Highland_purchase_indent.purchase_indent_action_window').id
		base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
		if base_url:
			base_url += \
				'/web?#id=%s&view_type=form&models=%s&menu_id=%s&action=%s' % (
					self.id, self._name, menu_id, action_id)
		return base_url

	@api.onchange('department_id')
	def onchange_department_id(self):
		for record in self:
			record.requestion_validater_id = False
			record.requestion_md_id = False
			record.store_manager_id = False
			record.account_user_id = False
			if record.department_id:
				record.requestion_validater_id = record.department_id.manager_id and record.department_id.manager_id.id or False
				record.store_manager_id = record.department_id.manager_id and record.department_id.manager_id.id or False
				record.requestion_md_id = record.department_id.manager_id and record.department_id.manager_id.id or False
				record.purchase_user_id = record.department_id.manager_id and record.department_id.manager_id.id or False
				record.account_user_id = record.department_id.manager_id and record.department_id.manager_id.id or False

	def requestion_approval_send_mail(self,email):
		mtp =self.env['mail.template']
		ir_model_data = self.env['ir.models.data']
		template_id = ir_model_data.get_object_reference('Highland_purchase_indent', 'purchase_indent_approval_request')
		mail_tem=mtp.browse(template_id[1])
		mail_tem.write({'email_to': email})
		mail_tem.send_mail(self.id,True)
		return True

	def indent_reject_send_mail(self,email):
		mtp =self.env['mail.template']
		ir_model_data = self.env['ir.models.data']
		template_id = ir_model_data.get_object_reference('Highland_purchase_indent', 'indent_reject_mail')
		mail_tem=mtp.browse(template_id[1])
		mail_tem.write({'email_to': email})
		mail_tem.send_mail(self.id,True)
		return True 

	def action_in_progress(self):
		self.ensure_one()
		if not self.prod_ids:
			raise UserError(_("You cannot confirm '%s' because there is no product line.", self.name))
		if self.requestion_validater_id and self.requestion_validater_id.work_email:
			self.requestion_approval_send_mail(self.requestion_validater_id.work_email)
		self.write({'state': 'in_progress'})

	def submit_department_validate(self):
		if self.store_manager_id and self.store_manager_id.employee_id and  self.store_manager_id.employee_id.work_email:
			self.requestion_approval_send_mail(self.store_manager_id.employee_id.work_email)
		self.state = 'department_validate'
		return True

	def submit_to_store_manager(self):
		if self.account_user_id and self.account_user_id.employee_id and  self.account_user_id.employee_id.work_email:
			self.requestion_approval_send_mail(self.account_user_id.employee_id.work_email)
		self.state = 'store_manager'
		return True

	@api.depends('state','department_id')
	def get_store_manager_flag(self):
		for data in self:
			data.store_manager_flag = False
			store_manager = data.store_manager_id and data.store_manager_id.id or False  
			if self.env.user.id == store_manager:
				data.store_manager_flag = True

	@api.depends('state','department_id')
	def get_department_flag(self):
		for data in self:
			data.department_flag = False
			department_user = data.requestion_validater_id and data.requestion_validater_id.user_id and data.requestion_validater_id.user_id.id or False
			if self.env.user.id == department_user:
				data.department_flag = True

	api.depends('state','department_id')
	def get_account_manager_flag(self):
		for data in self:
			data.account_manager_flag = False
			account_manager = data.account_user_id and data.account_user_id.id or False  
			if self.env.user.id == account_manager:
				data.account_manager_flag = True

	def submit_account_validate(self):
		if self.requestion_md_id and  self.requestion_md_id.work_email:
			self.requestion_approval_send_mail(self.requestion_md_id.work_email)
		self.state = 'account'
		return True

	@api.depends('state','department_id')
	def get_md_flag(self):
		for data in self:
			data.md_flag = False
			md_user = data.requestion_md_id and data.requestion_md_id.user_id and data.requestion_md_id.user_id.id or False 
			if self.env.user.id == md_user:
				data.md_flag = True

	def new_quotation(self):
		view = self.env.ref('Highland_purchase_indent.form_indent_wizard')
		return {
			'name': _('New Tender'),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'indent.quotation',
			'views': [(view.id, 'form')],
			'view_id': view.id,
			'target': 'new',
		}

	def transfer_products(self):
		view = self.env.ref('Highland_purchase_indent.form_transfer_products')
		return {
			'name': _('Transfer Products'),
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'transfer.products',
			'views': [(view.id, 'form')],
			'view_id': view.id,
			'target': 'new',
		}
	
	
	
	
	def get_purchase_tender(self):
		"""Purchase smart button"""
		self.ensure_one()
#		len(self.purchase_requisition_ids and self.purchase_requisition_ids.ids)
		return {
			'type': 'ir.actions.act_window',
			'name': 'Purchase Requisition',
			'view_mode': 'tree,form',
			'res_model': 'purchase.requisition',
			'domain': [('id', 'in', self.purchase_requisition_ids and self.purchase_requisition_ids.ids )],
			'context': "{'create': False}"
		}

	def get_picking(self):
		"""Picking smart button"""
		self.ensure_one()
		return {
			'type': 'ir.actions.act_window',
			'name': 'Picking',
			'view_mode': 'tree,form',
			'res_model': 'stock.picking',
			'domain': [('indent_id', '=', self.id)],
			'context': "{'create': False}"
		}

	def button_reject(self):
		form_view = self.env.ref('Highland_purchase_indent.reject_remark_view_id')
		return {
				'name': "Reject Remarks",
				'view_mode': 'form',
				'view_type': 'form',
				'view_id': form_view.id,
				'res_model': 'reject.remark',
				'type': 'ir.actions.act_window',
				'target': 'new',
			}

	@api.depends('state','department_id')
	def get_po_flag(self):
		for data in self:
			data.purchase_user_flag = False
			po_user = data.purchase_user_id and data.purchase_user_id.id or False 
			if self.env.user.id == po_user:
				data.purchase_user_flag = True


class ProductDetails(models.Model):
	_name = "product.details"
	_description = "Product Details"


	product_id = fields.Many2one('product.product', string='Product', required=True)
	name = fields.Char(string='Description',related='product_id.name')
	available_qty = fields.Integer(string='Available Qty')
	product_qty = fields.Float(string='Required Qty', digits='Product Unit of Measure', 
								required=True, default='1')
	product_uom = fields.Many2one(related='product_id.uom_id', string='Unit of Measure',)
	# partner_id = fields.Many2one('res.partner', string='Vendor')
	# cost_center = fields.Char('Cost Center')
	is_purchase = fields.Boolean(string='Need Purchase',readonly=True)
	code = fields.Char('Code', readonly=True)
	schedule_date = fields.Date(string='Scheduled Date')
	price_unit = fields.Float(string='Unit Price', digits='Product Price')
	prod_id = fields.Many2one('purchase.indent',string="Product Details")


	@api.onchange('product_id','product_qty')
	def onchange_product_id(self):
		if self.product_id:
			self.code = self.product_id.default_code
			self.write({'available_qty':self.product_id.qty_available})
			if self.product_qty > self.available_qty:
				self.write({'is_purchase':True})
			else:
				self.write({'is_purchase':False})



class IndentQuotation(models.TransientModel):
	_name = 'indent.quotation'
	_description = "Indent Quotaion"
	
	
	
	def default_get(self, fields_list):
		res = super(IndentQuotation, self).default_get(fields_list)
		line_date = []
		for pi in self.env['purchase.indent'].browse(self._context.get('active_ids')):
			for line in pi.prod_ids:
				line_date.append((0,0,{
											'pi_number':pi.name,
											'product_id':line.product_id and line.product_id.id or False,
											'code':line.code or ' ',
											'name':line.name,
											'product_qty':line.product_qty,
											'available_qty':line.available_qty,
											'price_unit':line.price_unit
										}))
		res.update({'indent_quotation_ids':line_date})
		return res

	indent_quotation_ids = fields.One2many('indent.quotation.line','indent_quotation_id', string='Indent Quotation Line')
#	category_id = fields.Many2one('partner.category', string='Vendor Category', required=True)
#	date = fields.Date(string='Response Date', index=True, default=datetime.today())
#	partner_ids = fields.Many2many('res.partner', string="Vendors")

#	@api.onchange('category_id') 
#	def _onchange_category_id(self):
#		if self.category_id:
#			partner_obj = self.env["res.partner"].search([('partner_category_id', '=', self.category_id.id)])
#			if partner_obj:
#				list_a = []
#				for rec in partner_obj:
#					list_a.append(rec.id)
#				self.write({'partner_ids': [(6,0, list_a)]})

	def create_quotation(self):
		active_id = self.env.context.get('active_ids')
		po_lines = []
		po_ids = []
		pr_id = False		
		for line in self.indent_quotation_ids:
			po_lines.append((0,0,{'product_id': line.product_id.id,
								  'code':line.code,
								  'pi_number':line.pi_number,
								  'product_description_variants':line.name,
								  'product_qty': line.product_qty - line.available_qty,
								  'price_unit':line.price_unit,
								  }))
		pr_id = self.env['purchase.requisition'].create({
					'user_id': self.env.user.id,
					'state':'draft'
					})
		pr_id.line_ids = po_lines
		for poi in self.env['purchase.indent'].browse(active_id):
			poi.purchase_requisition_ids = [(4,pr_id and pr_id.id)]
		return True
			
		
		
			

	def create_send_quotation(self):
		active_id = self.env.context.get('active_ids')
		for poi in self.env['purchase.indent'].browse(active_id):
			if poi.state != 'md_validated':
				raise UserError(_("You cannot create new quotation state must be 'Md Validated' '%s'", poi.name))
			for vendors in self.partner_ids:
				if poi.indent_type == 'normal':
					purchase = self.env['purchase.order'].create({
							'partner_id': vendors.id,
							'partner_category_id': self.category_id.id,
							'response_date': self.date,
							'indent_id': poi.id,
							'cost_center_id': poi.cost_center_id.id,
							'state':'waiting_for_approval1'
							})
					for line in poi.prod_ids:
						purchase_line = self.env['purchase.order.line'].create({
							'product_id': line.product_id.id,
							'product_qty': line.product_qty - line.available_qty,
							'order_id': purchase.id,
						})
				if poi.indent_type == 'emergency':
					purchase = self.env['purchase.order'].create({
							'partner_id': vendors.id,
							'partner_category_id': self.category_id.id,
							'response_date': self.date,
							'indent_id': poi.id,
							'cost_center_id': poi.cost_center_id.id,
							})
					for line in poi.prod_ids:
						purchase_line = self.env['purchase.order.line'].create({
							'product_id': line.product_id.id,
							'product_qty': line.product_qty - line.available_qty,
							'order_id': purchase.id,
						})
					purchase.button_confirm()
				poi.purchase_id = purchase.id

				template_id = self.env.ref('purchase.email_template_edi_purchase')
				template_id.sudo().send_mail(purchase.id, force_send=True)


class IndentQuotation_line(models.TransientModel):
	_name = 'indent.quotation.line'
	_description = "Indent Quotaion Line"
	
	indent_quotation_id = fields.Many2one('indent.quotation',string= 'Indent Quotaion')
	pi_number = fields.Char(string='Indent Number')
	product_id = fields.Many2one('product.product',string= 'Product')
	code = fields.Char(string='Code')
	name = fields.Char(string='Description')
	product_qty = fields.Integer(string='Product Qty')
	available_qty = fields.Integer(string='Available Qty')
	price_unit = fields.Float(string='Price Unit')
	

class TransferProducts(models.Model):
	_name = 'transfer.products'
	_description = "Transfer Products"


	picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', required=True)
	location_id = fields.Many2one('stock.location', "Source Location", required=True)
	location_dest_id = fields.Many2one('stock.location', "Destination Location", required=True)


	def create_transfer(self):
		active_id = self.env.context.get('active_id')
		rec = self.env['purchase.indent'].browse(int(active_id))
		picking = self.env['stock.picking'].create({
				'picking_type_id': self.picking_type_id.id,
				'location_id': self.location_id.id,
				'location_dest_id': self.location_dest_id.id,
				'origin': rec.name,
				'indent_id': rec.id,
				'state':'draft'
				})
		for line in rec.prod_ids:
			picking_line = self.env['stock.move'].create({
				'name': line.product_id.name,
				'product_id': line.product_id.id,
				'product_uom': line.product_uom.id,
				'location_id': picking.location_id.id,
				'location_dest_id': picking.location_dest_id.id,
				'product_uom_qty': line.product_qty,
				'picking_id': picking.id,
				})
		picking.action_confirm()
		rec.picking_id = picking.id
