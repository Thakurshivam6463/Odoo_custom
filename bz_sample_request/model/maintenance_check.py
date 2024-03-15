# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

  # For configuration menu checklist
  ######################################

class MaintenanceCheck(models.Model):
    _name = 'maintenance.check'
    _description = "Maintenance Checklist"


    name = fields.Char(string="Name")

