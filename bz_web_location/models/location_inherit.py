# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LocationInherit(models.Model):
    _inherit = "product.template"

    location = fields.Many2many(
        'location.conf', 'location_conf_rel',
        'product_id', 'city_id',
        string='Location')


