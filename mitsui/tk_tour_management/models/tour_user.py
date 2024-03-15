# -*- coding: utf-8 -*-

from odoo import fields, api, models


class TourCustomer(models.Model):
    _inherit = 'res.partner'


class TourEmployee(models.Model):
    _inherit = 'hr.employee'
