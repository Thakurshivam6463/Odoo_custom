# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class reports(models.Model):
    _name = "management.reports"
    _description = "Management Reports"

    name = fields.Char(string='Student Name')
    course = fields.Char(string='Course')
    branch = fields.Char(string='Branch')
    batch= fields.Char(string='Batch')
