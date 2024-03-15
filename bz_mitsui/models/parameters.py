# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProtocolParameter(models.Model):
    _name = "protocol.parameter"
    _description = "Protocol Parameter"
    _rec_name = 'name'

    name = fields.Char(string='Parameter')
