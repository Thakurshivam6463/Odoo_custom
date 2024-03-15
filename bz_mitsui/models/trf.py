# -*- coding: utf-8 -*-is_check
from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError


class TrfInherit(models.Model):
    _inherit = "document.details"

    standard_id = fields.Many2one('standards', string="Standard to be Followed")


class ScopeInherit(models.Model):
    _inherit = "test.scope"

    standard_id = fields.Many2one('standards', string="Standard")


class ProjectTaskInherit(models.Model):
    _inherit = "project.task.template"

    standard_id = fields.Many2one('standards', string="Standard", required=True)

    # @api.onchange('standard_id')
    # def onchange_task_standard_id(self):
    #     if self.standard_id:
    #         self.name = self.standard_id.name


class ProjectCustomInherit(models.Model):
    _inherit = "project.task.custom"

    name = fields.Many2one('task.description', string="Name", required=True)
    protocol_id = fields.Many2one('protocol.form', string="Protocol")
    result_compilation = fields.Html(string='Result Compilation')


    @api.onchange('name')
    def onchange_task_name(self):
        if self.name:
            self.description = self.name.description
            self.result_compilation = self.name.result_compilation





