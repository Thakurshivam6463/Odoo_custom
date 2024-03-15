# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

  # For configuration menu checklist
  ######################################

class MaintenanceCheckSheet(models.Model):
    _name = 'maintenance.checksheet'
    _description = "Maintenance Checklist"
    _rec_name = 'check_point'


    check_point = fields.Char(string="Check Point")




class ActionCheckSheet(models.Model):
    _name = 'action.checksheet'
    _description = "Action Checklist"
    _rec_name = 'action_sheet'

    action_sheet = fields.Char(string="Action")


