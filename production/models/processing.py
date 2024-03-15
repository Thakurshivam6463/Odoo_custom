# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class FishProcessing(models.Model):
    _name = 'fish.processing'
    _rec_name = 'number'    

    number = fields.Char(string="Number")
    user_id = fields.Many2one('res.partner', string="Processed By")
    processing_date = fields.Date(string="Processing Date")
    note = fields.Char(string="Note")
