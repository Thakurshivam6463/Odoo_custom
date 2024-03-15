# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class SoakOutDetails(models.Model):
    _name = 'soak.out'
    _rec_name = 'date'

    date = fields.Date(string="End Date")
    end_time = fields.Many2one('start.time', string="End Time")

    soak_details_ids = fields.One2many('soak.detail', 'soak_details_id', string="Soak details ids")
    soak_id = fields.Many2one("fish.production", string="Soak")
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'), ('complete', 'Complete'),
         ('cancel', 'Cancel'),],
        default='draft', string="Status")

    def action_draft(self):
        self.state = 'draft'

    def action_submit(self):
        self.state = 'submit'

    def action_complete(self):
        self.state = 'complete'

    def action_cancel(self):
        self.state = 'cancel'



class SoakDetails(models.Model):
    _name = 'soak.detail'

    soak_details_id = fields.Many2one('soak.out', string="Soak Details", invisible=True)

    grade = fields.Many2one('grade.count', string="Grade")
    value_add_product = fields.Many2one('valueadd.product', string="Value Add Product")
    quantity = fields.Float(string="Quantity")
    sock_in = fields.Boolean(string="Sock In")
    sock_out_qty = fields.Text(string="Sock Out Quantity")
    pickup = fields.Char(string="Pickup")
