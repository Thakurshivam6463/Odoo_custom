# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError


class MaintenanceFrom(models.Model):
    _inherit = "maintenance.request"

    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    planned_start = fields.Date(string='Planned Start Date', default=datetime.date.today())
    planned_end = fields.Date(string='Planned End Date', default=datetime.date.today())
    actul_start = fields.Date(string="Actual Start Date", default=datetime.date.today())
    actul_end = fields.Date(string="Actual End Date", default=datetime.date.today())

    @api.onchange('planned_start', 'planned_end', 'actul_start', 'actul_end')
    def date_onchange(self):
        current_date = datetime.date.today()
        for rec in self:
            if rec.planned_start > rec.planned_end:
                raise ValidationError(_("Planned End Date can not be lower than Planned Start Date"))
            if rec.planned_start < current_date:
                raise ValidationError(_("Planned Start Date can not be lower than Current Date"))
            if rec.actul_start > rec.actul_end:
                raise ValidationError(_("Actual End Date can not be lower than Actual Start Date"))
            if rec.actul_start < rec.planned_start:
                raise ValidationError(_("Actual Start Date can not be lower than Planned Start Date"))





