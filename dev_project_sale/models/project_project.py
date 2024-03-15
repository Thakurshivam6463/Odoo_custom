# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api


class project_project(models.Model):
    _inherit = 'project.project'
    
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    is_create_testing = fields.Boolean('Create Testing')
    
    
    
    
    
    
    def create_testing(self):
        rec_id = self.env['dev.create.testing'].create({
            'project_id':self.id,
            'sale_id':self.sale_id and self.sale_id.id or False,
        })
        for line in self.sale_id.testing_lines:
            val={
                'line_id':line.id,
                'testing_id':line.testing_id and line.testing_id.id or False,
                'checklist_ids':[(6,0, line.checklist_ids.ids)],
                'location_id':line.location_id and line.location_id.id or False,
                'create_testing_id':rec_id and rec_id.id or False
            }
            self.env['create.testing.line'].create(val)
        return {
            'view_mode': 'form',
            'res_id': rec_id.id,
            'res_model': 'dev.create.testing',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

class task_task(models.Model):
    _inherit = 'project.task'
    _order = "priority desc"
    
    #checklist_lines = fields.One2many('task.checklist.line','task_id', string='Checklist')
    # checklist_progress = fields.Float(string='Testing Progress', compute='_checklist_progress_status')
    # result_lines = fields.One2many('task.result.lines','task_id', string='Results')
    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    
    
    # @api.depends('checklist_lines','checklist_lines.is_check')
    # def _checklist_progress_status(self):
    #     for task in self:
    #         total_checklists = len(task.checklist_lines)
    #         task_checklists = 0
    #         for l in task.checklist_lines:
    #             if l.is_check:
    #                 task_checklists += 1
    #         progress = 0
    #         if total_checklists > 0:
    #             progress = (task_checklists * 100) / total_checklists
    #         task.checklist_progress = progress
            
            


# class task_checklists_lines(models.Model):
#     _name = 'task.checklist.line'
#
#     checklist_id = fields.Many2one('testing.checklist', string='Checklist')
#     is_check = fields.Boolean('IS Checked')
#     task_id = fields.Many2one('project.task', string='Task')
#
# class result_lines(models.Model):
#     _name = 'task.result.lines'
#
#     name = fields.Char('Name', required="1")
#     result = fields.Char('Result', required="1")
#     task_id = fields.Many2one('project.task', string='Task')


   
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
