# -*- coding: utf-8 -*-

#############################################################################

from odoo import models, fields, api, _


class Project(models.Model):
    _inherit = 'project.project'

    project_template_id = fields.Many2one('project.task.template',string="Project Template Id")

    def create_task(self, item, parent):
        vals = {'project_id': self.id,
                'name': item.name.name,
                'parent_id': parent,
                'stage_id': self.env['project.task.type'].search([('sequence', '=', 1)], limit=1).id,
                # 'user_id': item.user_ids.id,
                'description': item.description,
                'abbreviations_id': item.abbreviations_id.id,
                'protocol_id': item.protocol_id.id,
                'result_compilation': item.result_compilation,
                }
        task_id = self.env['project.task'].create(vals).id
        for sub_task in item.child_ids:
            self.create_task(sub_task, task_id)

    def action_create_project_from_template(self):
        template_id = self.project_template_id
        for item in template_id.task_ids:
            self.create_task(item, False)
        return {
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'context': self._context
        }


class ProjectTaskCustom(models.Model):
    _name = 'project.task.custom'

    # name = fields.Char("Name", required=True)
    name = fields.Char(string="Name", required=True)
    #task_id = fields.Many2one('task.description', string=" Name")
    project_template_id = fields.Many2one('project.task.template')
    description = fields.Html("Task Description")
    # user_ids = fields.Many2many('res.users', relation='project_task_custom_user_rel', column1='task_id',
    #                             column2='user_id',
    #                             string='Assignees', tracking=True)
    # user_ids = fields.Many2many('res.users', string='Assignee', tracking=True)
    equipment_id = fields.Many2one('maintenance.equipment', string=" Equipment")
    abbreviations_id = fields.Many2one('abbreviations', string='Abbreviation')
    #protocol_id = fields.Many2one('protocol.form',string="Protocol")

    parent_id = fields.Many2one('project.task.custom', string='Parent Task', index=True)
    child_ids = fields.One2many('project.task.custom', 'parent_id', string="Sub-tasks")

    def action_open_task(self):
        return {
            'view_mode': 'form',
            'res_model': 'project.task.custom',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'context': self._context
        }

    


class ProjectTaskTemplate(models.Model):
    _name = 'project.task.template'

    name = fields.Char(string="Name", translate=True)
    task_ids = fields.One2many('project.task.custom', 'project_template_id', string="Tasks")
