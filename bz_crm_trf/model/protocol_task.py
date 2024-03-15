# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProtocolButtonFrom(models.Model):
    _inherit = ["project.task"]

    protocol_count = fields.Integer('PROTOCOL Count', compute="_compute_protocol_count")
    equipment_id = fields.Many2one('maintenance.equipment', string=" Equipment")
    # protocol_view_id = fields.Many2one('protocol.form', string="protocol view")
    protocol_id = fields.Many2one('protocol.form', string="Protocol")


    def action_protocol_form_new(self):
        ctx = {
            'default_task_id': self.id,
            'default_date': self.create_date,

        }
        return {
            "name": _("PROTOCOL"),
            "view_mode": "form",
            "res_model": "protocol.form",
            "type": "ir.actions.act_window",
            'context': ctx,
        }

    def action_samplein(self):
        line_val = []
        for line in self.project_id.product_ids:
            line_val.append((0, 0, {'product_id': line.product_id.id,
                                    'source_location': line.source_location.id,
                                    # 'destination_location': line.destination_location.id,
                                    'qty': line.qty
                                    }))
        ctx = {
            'default_sample_line_ids': line_val
        }

        return {
            "name": _("Sample In/Out"),
            "view_mode": "form",
            "res_model": "wizard.sample.move",
            "type": "ir.actions.act_window",
            "context": ctx,

        }

    def _compute_protocol_count(self):
        if self.ids:
            scope_data = self.env['protocol.form'].sudo().read_group([
                ('task_id', 'in', self.ids)
            ], ['task_id'], ['task_id'])
            mapped_data = {m['task_id'][0]: m['task_id_count'] for m in scope_data}
        else:
            mapped_data = dict()
        for scope in self:
            scope.protocol_count = mapped_data.get(scope.id, 0)


    def action_protocol_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "PROTOCOL",
            "res_model": "protocol.form",
            "domain": [("task_id", "=", self.id)],
            "view_mode": "tree,form",
            'target': 'current',
        }

class ProjectInherit(models.Model):
    _inherit = "project.project"

    project_type = fields.Selection([
        ('bis', 'BIS'),
        ('non_bis', 'Non BIS'),
    ],)


