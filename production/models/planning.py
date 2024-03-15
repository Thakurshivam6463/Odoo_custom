# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class FishPlanning(models.Model):
    _name = 'fish.planning'
    _rec_name = 'number'

    number = fields.Char("Grade Name", default=lambda self: self.env['ir.sequence'].next_by_code('grade.operation'))
    user_id = fields.Many2one('res.partner', string="Planner")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
