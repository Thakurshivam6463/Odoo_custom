# -*- coding: utf-8 -*-
from odoo import api, fields, models


class WizardEquipment(models.TransientModel):
    _name = "wizard.equipment"
    _description = "Wizard Equipment"

    project_id = fields.Many2one('project.project', string="Project")
    task_ids = fields.Many2many('project.task', string="Task")
    assigned_to = fields.Many2one('res.users', string="Assigned to")
    deadline = fields.Date(string="Deadline")
    customer = fields.Many2one('res.partner', string="Customer")

    @api.onchange('project_id')
    def onchange_project_id(self):
        if self.project_id:
            task_ids = self.env['project.task'].search([('project_id', '=', self.project_id.id)]).ids
            self.task_ids = [(6,0, task_ids)]
            self.customer = self.project_id.partner_id.id
            self.assigned_to = self.project_id.user_id.id


    def action_create_task(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            equipment = self.env['maintenance.equipment'].browse(active_id)
            task_ids = self.env['project.task'].search([('project_id', '=', self.project_id.id)])
            for task in task_ids:
                task.equipment_id = equipment.id
















