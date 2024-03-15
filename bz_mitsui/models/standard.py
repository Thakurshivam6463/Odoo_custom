# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Standard(models.Model):
    _name = "standards"
    _description = "Standard"
    _rec_name = 'name'

    name = fields.Char(string=" Standard ")


