# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Abbreviations(models.Model):
    _name = "abbreviations"
    _description = "Abbreviations"
    _rec_name = 'mcind'

    mcind = fields.Char(string=" Abbreviations")
    mitsui_chemicals = fields.Char(string=' Word/phrase')


