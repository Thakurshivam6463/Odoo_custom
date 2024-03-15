# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Abbreviations(models.Model):
    _name = "task.description"
    _description = "Task Description"
    _rec_name = 'name'

    name = fields.Char(string="Task")
    description = fields.Html(string='Description')
    result_compilation = fields.Html(string='Result Compilation')



