# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class create_testing(models.TransientModel):
    _name = 'dev.create.testing'
    _description = 'Create Testing'
    
    name = fields.Char('Name')
    line_ids = fields.One2many('create.testing.line','create_testing_id', string='Testing Lines')
    project_id = fields.Many2one('project.project', string='Project')
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    
    
    def action_create_testing(self):
        for line in self.line_ids:
            if not line.user_id:
                raise ValidationError(_('Please Assign user for testing.'))
        parent_id = False
        for line in self.line_ids:
            che_lst = []
            for check in line.checklist_ids:
                che_lst.append((0,0,{
                    'checklist_id':check.id,
                }))
            vals={
                'name':line.testing_id.name or '',
                'project_id':self.project_id and self.project_id.id or False,
                'parent_id':parent_id and parent_id.id or False,
                'user_id':line.user_id and line.user_id.id or False,
                'partner_id':self.sale_id and self.sale_id.partner_id.id or False,
                'checklist_lines':che_lst,
            }
            parent_id = self.env['project.task'].create(vals)
            
    
class create_testing_line(models.TransientModel):
    _name = 'create.testing.line'
    _description = 'Create Testing Lines'
    
    line_id= fields.Many2one('project.testing', string='Project Testing')
    testing_id = fields.Many2one('dev.testing', string='Testing')
    checklist_ids = fields.Many2many('testing.checklist', string='Checklist')
    location_id = fields.Many2one('dev.testing.location', string='Location')
    create_testing_id = fields.Many2one('dev.create.testing', string='Create Testing')
    user_id = fields.Many2one('res.users', string='Assign')
    
    
    
    
    
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
