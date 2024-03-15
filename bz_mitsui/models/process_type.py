# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProcessType(models.Model):
    _name = "process.type"
    _description = "Process Type"
    _rec_name = 'name'

    name = fields.Char(string=" Test Type")
