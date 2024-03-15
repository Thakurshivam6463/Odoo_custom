from odoo import models, api, _, fields

class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    cost_center = fields.Char('Cost Center')
    work_center = fields.Char('Work Center')

    @api.model
    def check_purchase_requisition_draft(self):
        total_po_requisition_draft = self.env['purchase.requisition'].search([('state', '=', 'draft')])
        return {
            'total_po_requisition_draft': len(total_po_requisition_draft)
        }

    @api.model
    def check_purchase_requisition_confirmed(self):
        total_po_requisition_confirmed = self.env['purchase.requisition'].search([('state', '=', 'in_progress')])
        return {
            'total_po_requisition_confirmed': len(total_po_requisition_confirmed)
        }

    @api.model
    def check_purchase_requisition_ongoing(self):
        total_po_requisition_ongoing = self.env['purchase.requisition'].search([('state', '=', 'ongoing')])
        return {
            'total_po_requisition_ongoing': len(total_po_requisition_ongoing)
        }

