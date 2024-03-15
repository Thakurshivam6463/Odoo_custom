# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class FishQC(models.Model):
    _name = 'fish.qc'
    _rec_name = 'number'

    number = fields.Char(string="Number")
    user_id = fields.Many2one('res.partner', string="Responsible Person")
    reviewer_id = fields.Many2one('res.partner', string="Reviewed By")
    review_date = fields.Date(string="Review Date")
    review_stage = fields.Selection([
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('hold', 'Hold'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Reviewed Stage")
    receiving_id = fields.Many2one('materials.reciving.deck', 'Materials Receiving')
    sample_weight = fields.Float('Sample Weight')
    percentage = fields.Float('Percentage')
    materials_type = fields.Many2one('materials.type', string="Type", required=True)
    photos = fields.Binary(string="Photos")
