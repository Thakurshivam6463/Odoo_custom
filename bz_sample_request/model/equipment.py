# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EquipmentButtonFrom(models.Model):
    _inherit = "maintenance.equipment"

    equipment_count = fields.Integer('Equipment Count', compute="_compute_equipment_count")

    def action_equipment(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Tasks",
            "res_model": "project.task",
            "domain": [("equipment_id", "=", self.id)],
            "view_mode": "tree,form",
            'target': 'current',
        }
    def _compute_equipment_count(self):
        if self.ids:
            scope_data = self.env['project.task'].sudo().read_group([
                ('equipment_id', 'in', self.ids)
            ], ['equipment_id'], ['equipment_id'])
            mapped_data = {m['equipment_id'][0]: m['equipment_id_count'] for m in scope_data}
        else:
            mapped_data = dict()
        for scope in self:
            scope.equipment_count = mapped_data.get(scope.id, 0)

    def action_equipment_new(self):
        return {
            "name": _("Task"),
            "view_mode": "form",
            "res_model": "wizard.equipment",
            "type": "ir.actions.act_window",
            "target": 'new',

        }