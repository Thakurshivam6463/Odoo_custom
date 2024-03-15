# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ScopeMatrix(models.Model):
    _name = "scope.matrix"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Scope Matrix"
    _rec_name = 'sequence'

    sequence = fields.Char(string='Sequence No.', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    date_requested = fields.Date(string='Date Requested')
    assign_user = fields.Many2one('res.partner', string="Assign User")
    requested_user = fields.Many2one('res.partner', string='Requested User')
    trf_reference = fields.Char(string='TRF Reference No.')
    note = fields.Text(string='Note')
    buffer_time = fields.Integer(string='Buffer time')
    compiling_data_results_interpretation_of_results = fields.Integer(string="Compiling data, Results Interpretation of results")
    preparation_of_report = fields.Integer(string="Preparation of Report")
    total_project_time = fields.Float(string="Total Project Time ( in hrs.and days)")

    batch_scope_matrix_ids = fields.One2many('test.scope', 'scope_matrix_id', string="Batch Scope Matrix", invisible=True)
    state = fields.Selection([('draft', 'Draft'), ('requested', 'Requested'), ('approved', 'Approved'), ('done', 'Done'), ('cancel', 'Cancelled')],
                             default='draft', string="Status", tracking=True)
    trf_id = fields.Many2one("trf", string="TRF")

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

    @api.onchange('total_project_time', 'buffer_time', 'compiling_data_results_interpretation_of_results', 'preparation_of_report')
    def onchange_total_project_time(self):
        a = 0
        if self.batch_scope_matrix_ids:
            for line in self.batch_scope_matrix_ids:
                a += line.duration_in_days
        self.total_project_time = self.buffer_time + self.compiling_data_results_interpretation_of_results + self.preparation_of_report + a





class TestScope(models.Model):
    _name = "test.scope"
    _description = "Test Scope"

    product_id = fields.Many2one('product.product', string='Samples')
    test_description = fields.Char(string='Test Description')
    time = fields.Float(string="Time (hrs) per one module")
    frequency = fields.Integer(string="Frequency")
    quantity = fields.Integer(string="System Voltage")
    total_time = fields.Float(string="Total time")
    duration_in_days = fields.Float(string="Duration in days")
    equipment_software_required = fields.Char(string='Equipment, Software required')
    manpower_required = fields.Char(string="Manpower required")
    remarks = fields.Text(string="Remarks")
    sub_contracting_required = fields.Char(string="Sub-contracting required")
    scope_matrix_id = fields.Many2one('scope.matrix', string="Batch Scope Matrix", invisible=True)





