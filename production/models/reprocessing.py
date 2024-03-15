# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class FishReprocessing(models.Model):
    _name = 'fish.reprocessing'
    _rec_name = 'number'

    number = fields.Char(string="Number")
    user_id = fields.Many2one('res.partner', string="Process By")
    re_process_user_id = fields.Many2one('res.partner', string="ReProcess By")
    reason = fields.Char(string="Reason of Re-Process")
