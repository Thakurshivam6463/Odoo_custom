from odoo import models, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sample_request_count = fields.Integer('# Sample Request', compute='_compute_sample_request_count')
    project_template_id = fields.Many2one('project.task.template', string="Project Template")
    remarks = fields.Text(string="Remarks/Comments")


    def _compute_sample_request_count(self):
        if self.ids:
            scope_data = self.env['sample.form'].sudo().read_group([
                ('sm_id', 'in', self.ids)
            ], ['sm_id'], ['sm_id'])
            mapped_data = {m['sm_id'][0]: m['sm_id_count'] for m in scope_data}
        else:
            mapped_data = dict()
        for scope in self:
            scope.sample_request_count = mapped_data.get(scope.id, 0)

    def action_sam_req(self):
        sale_ids = self.env['project.project'].search([('sale_order_id', '=', self.id)])
        ctx = {
            'default_customer_id': self.partner_id.id,
            'default_sm_id': self.id,
            'default_sale_order_id': self.id,
            'default_project_id': sale_ids.id,
            'default_test_request_no': self.scope_matrix_id.trf_reference
        }
        return {
            "name": _("Sale Sample Request"),
            "view_mode": "form",
            "res_model": "sample.form",
            "type": "ir.actions.act_window",
            'context': ctx,
        }

    def action_view_sp_rq(self):
        return {
            "name": _("Sale Sample Request"),
            "view_mode": "tree,form",
            "res_model": "sample.form",
            "type": "ir.actions.act_window",
            'domain': [('sm_id', 'in', self.ids)]
        }
