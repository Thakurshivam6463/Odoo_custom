# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TourInquiry(models.Model):
    _inherit = 'crm.lead'

    package_id = fields.Many2one('tour.package', string='Package')
    booking_id = fields.Many2one('tour.booking', string='Booking No.')
