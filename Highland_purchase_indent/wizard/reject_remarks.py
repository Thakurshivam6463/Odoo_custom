# -*- coding: utf-8 -*-
from odoo import fields, models, api


class  RejectRemark(models.TransientModel):
	_name = 'reject.remark'
	_description = 'Reject remark Wizard'

	name = fields.Text('Remarks',required=True)


	def action_reject_remark(self):
		active_id = self.env.context.get('active_id')
		rec = self.env['purchase.indent'].browse(int(active_id))
		rec.indent_reject_send_mail(rec.employee_id.work_email)
		rec.write({'rejected_remarks':self.name,'state':'rejected',
					'rejected_user':self.env.user})