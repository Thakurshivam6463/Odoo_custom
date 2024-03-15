# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class CollegeStudent(models.Model):
    _name = "college.student"
    _description = "College Student"

    name = fields.Char(string='Name', tracking=True, required=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default='male', tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft', string="Status", tracking=True)


    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Student'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('college.student') or _('New')
        res = super(CollegeStudent, self).create(vals)
        return res

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'
