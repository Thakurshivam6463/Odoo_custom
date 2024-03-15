from odoo import models, api, _

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def check_rfq(self):
        total_rfq = self.env['purchase.order'].search([('state', '=', 'draft')])
        return {
            'total_rfq': len(total_rfq)
               }

    @api.model
    def check_purchase_order(self):
        total_po = self.env['purchase.order'].search([('state', '=', 'purchase')])
        return {
            'total_po': len(total_po)
        }

    @api.model
    def check_purchase_done(self):
        total_po_done = self.env['purchase.order'].search([('state', '=', 'done')])
        return {
            'total_po_done': len(total_po_done)
        }

    @api.model
    def check_purchase_cancel(self):
        total_po_cancel = self.env['purchase.order'].search([('state', '=', 'cancel')])
        return {
            'total_po_cancel': len(total_po_cancel)
        }

    @api.model
    def check_management_po(self):
        management_department_id = self.env['hr.department'].search([('name', '=', 'Management')])
        if management_department_id:
            user_ids = management_department_id.member_ids.user_id
        po_ids = self.env['purchase.order'].search([('user_id', 'in', user_ids.ids), ('state', '=', 'draft')])
        return {
            'total_management_po': len(po_ids),
            'management_po': po_ids.ids
        }

    @api.model
    def check_administration_po(self):
        administration_department_id = self.env['hr.department'].search([('name', '=', 'Administration')])
        if administration_department_id:
            user_ids = administration_department_id.member_ids.user_id
        po_ids = self.env['purchase.order'].search([('user_id', 'in', user_ids.ids), ('state', '=', 'draft')])
        return {
            'total_administration_po': len(po_ids),
            'administration_po': po_ids.ids
        }

    @api.model
    def check_sales_po(self):
        sales_department_id = self.env['hr.department'].search([('name', '=', 'Sales')])
        if sales_department_id:
            user_ids = sales_department_id.member_ids.user_id
        po_ids = self.env['purchase.order'].search([('user_id', 'in', user_ids.ids), ('state', '=', 'draft')])
        return {
            'total_sales_po': len(po_ids),
            'sales_po': po_ids.ids
        }