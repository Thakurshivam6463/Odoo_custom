# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ReportsWizard(models.TransientModel):
    _name = "management.reports.wizard"


    date_to = fields.Char(string='Date_To')
    date_from=fields.Char(string='Date_From')


