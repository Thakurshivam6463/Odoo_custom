# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError


class ScopeMatrix(models.Model):
    _name = "scope.matrix"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Scope Matrix"
    _rec_name = 'sequence'

    sequence = fields.Char(string='Sequence No.', required=False, copy=False, readonly=True, default=lambda self: _('New'))
    date_requested = fields.Date(string='Date Requested', default=datetime.date.today())
    assign_user = fields.Many2one('res.users', string="Assigned to Sales")
    requested_user = fields.Many2one('res.users', string='Requested User', default=lambda self: self.env.user.id)
    trf_reference = fields.Char(string='TRF Reference No.')
    note = fields.Text(string='Note')

    buffer_time = fields.Float(string='Buffer time')
    compiling_data_results_interpretation_of_results = fields.Float(string="Compiling data, Results Interpretation of results")
    preparation_of_report = fields.Float(string="Preparation of Report")
    total_project_time = fields.Float(string="Total Project Time ( in hrs.and days)", compute='_compute_duration', store=True)

    batch_scope_matrix_ids = fields.One2many('test.scope', 'scope_matrix_id', string="Batch Scope Matrix", invisible=True)
    state = fields.Selection([('draft', 'Draft'), ('requested', 'Requested'), ('approved', 'Approved'), ('done', 'Done'), ('cancel', 'Cancelled')],
                             default='draft', string="Status", tracking=True)
    trf_id = fields.Many2one("trf", string="TRF")
    quotation_count = fields.Integer('# Scope Matrix', compute='_compute_sale_count')
    duration_in_days = fields.Float(string="Total Duration in days")

    @api.depends('buffer_time', 'compiling_data_results_interpretation_of_results', 'preparation_of_report', 'duration_in_days')
    def _compute_duration(self):
        for line in self:
            line.total_project_time = self.buffer_time + self.compiling_data_results_interpretation_of_results + self.preparation_of_report + self.duration_in_days

    def _compute_sale_count(self):
        if self.ids:
            sale_data = self.env['sale.order'].sudo().read_group([
                ('scope_matrix_id', 'in', self.ids)
            ], ['scope_matrix_id'], ['scope_matrix_id'])
            mapped_data = {m['scope_matrix_id'][0]: m['scope_matrix_id_count'] for m in sale_data}
        else:
            mapped_data = dict()
        for scope in self:
            scope.quotation_count = mapped_data.get(scope.id, 0)

    def action_requested(self):
        self.state = 'requested'

    def action_approved(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('scope.matrix') or _('New')
        res = super(ScopeMatrix, self).create(vals)
        if self.env.context.get('active_id'):
            vvv = self.env.context.get('active_id')
            res.trf_id = vvv
        if self.env.context.get('ref'):
            bb = self.env.context.get('ref')
            res.trf_reference = bb
        return res

    # @api.onchange('total_project_time', 'buffer_time', 'compiling_data_results_interpretation_of_results', 'preparation_of_report')
    # def onchange_total_project_time(self):
    #     a = 0
    #     if self.batch_scope_matrix_ids:
    #         for line in self.batch_scope_matrix_ids:
    #             a += line.duration_in_days
    #     self.total_project_time = self.buffer_time + self.compiling_data_results_interpretation_of_results + self.preparation_of_report + a

    def action_sale_quotations_new(self):
        if not self.trf_id.name:
            return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
        else:
            return self.action_new_quotation()

    def action_new_quotation(self):
        line = []
        if self.batch_scope_matrix_ids:
            for req in self.batch_scope_matrix_ids:
                line.append((0, 0, {
                    'product_id': req.product_id.id,
                    'product_uom_qty': req.quantity,
                    'name': req.product_id.name,
                    'product_uom': req.product_id.uom_id.id,
                    'standard_id': req.standard_id.id,
                        }))
        action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.trf_id.contact_persons_name.id,
            'default_partner_id': self.trf_id.contact_persons_name.id,
            'default_campaign_id': self.trf_id.crm_id.campaign_id.id,
            'default_medium_id': self.trf_id.crm_id.medium_id.id,
            'default_origin': self.sequence,
            'default_source_id': self.trf_id.crm_id.source_id.id,
            #'default_project_template_id': self.standard_id.id,
            'default_company_id': self.env.company.id,
            'default_scope_matrix_id': self.id,
            'default_order_line': line
        }
        if self.trf_id.crm_id.team_id:
            action['context']['default_team_id'] = self.trf_id.crm_id.team_id.id,
        if self.trf_id.crm_id.user_id:
            action['context']['default_user_id'] = self.trf_id.crm_id.user_id.id
        return action

    def action_view_sale_quotation(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id
        }
        action['domain'] = [('opportunity_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]
        quotations = self.mapped('order_ids').filtered(lambda l: l.state in ('draft', 'sent'))
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action

    def action_sale_view(self):
        return {
            'type': "ir.actions.act_window",
            'name': 'Quotations',
            "res_model": "sale.order",
            "domain": [("scope_matrix_id", "=", self.id)],
            "view_mode": "tree,form",
            'target': 'current',
        }


class TestScope(models.Model):
    _name = "test.scope"
    _description = "Test Scope"

    product_id = fields.Many2one('product.product', string='Product')
    test_description = fields.Char(string='Test Description')
    time = fields.Float(string="Time (hrs) per one module")
    frequency = fields.Integer(string="Frequency")
    quantity = fields.Integer(string="Quantity")
    total_time = fields.Float(string="Total time")
    equipment_software_required = fields.Many2many('maintenance.equipment', string='Equipment, Software required')
    manpower_required = fields.Many2many('hr.employee',string="Manpower required")
    remarks = fields.Text(string="Remarks")
    sub_contracting_required = fields.Char(string="Sub-contracting required")
    #standard = fields.Char(string='Standard')
    scope_matrix_id = fields.Many2one('scope.matrix', string="Batch Scope Matrix", invisible=True)






