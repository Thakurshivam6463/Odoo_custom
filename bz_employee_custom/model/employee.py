# -*- coding: utf-8 -*-
from odoo import api, fields, models



class Employeee(models.Model):
    _inherit = "hr.employee"

    aadhar = fields.Char(string='Aadhar No.')