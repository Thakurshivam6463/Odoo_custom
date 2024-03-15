# -*- coding: utf-8 -*-

from odoo import models, fields


class CustomResCompany(models.Model):
    """ Add gst Number """
    _inherit = 'res.company'
    _description = 'Add gst Number'

    company_gst_number = fields.Char('GSTIN Number')