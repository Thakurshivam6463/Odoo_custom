# -*- coding: utf-8 -*-is_check
from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError


class MaintenanceChecklistFrom(models.Model):
    _inherit = "maintenance.request"

    manit_ids = fields.One2many('maintenance.checklist', 'manit_id', string="Equi", invisible=True)
    # checklist_progress = fields.Float(string='Checklist Progress', compute='_checklist_progress_status')
    description = fields.Text(string='Description')
    request_date = fields.Datetime('Request Date', tracking=True, default=fields.Date.context_today,
                               help="Date requested for the maintenance to happen")


class NewMaintenanceChecklistFrom(models.Model):
    _name = 'maintenance.checklist'

    checklist_id = fields.Many2one('maintenance.checksheet', string="Checklist")
    action_ids = fields.Many2many('action.checksheet', string=" Action")
    verification = fields.Selection(
        [('ok', 'OK'), ('not ok', ' Not Ok')],
        string="Verification")
    actions_taken = fields.Char(string="Actions taken")
    maintenance = fields.Char(string="Maintenance")
    intermidiate_check = fields.Char(string="Intermidiate Check")
    comments = fields.Char(string="Comments")

    manit_id = fields.Many2one('maintenance.request', string="Manit", invisible=True)

    # @api.onchange('checklist_id')
    # def onchange_maintenance_checklist_id(self):
    #     if self.checklist_id:
    #         self.description = self.checklist_id.description
    #
    # def action_draft(self):
    #     self.status = 'draft'
    #
    # def action_approved(self):
    #     self.status = 'approved'





