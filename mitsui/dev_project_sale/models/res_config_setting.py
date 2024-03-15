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

class res_company(models.Model):
    _inherit='res.company'
    
    project_stage_ids = fields.Many2many('project.task.type', string='Stages')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    project_stage_ids = fields.Many2many('project.task.type', related="company_id.project_stage_ids", string='Stages', readonly=False)
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
