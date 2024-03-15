# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LocationConf(models.Model):
    _name = "location.conf"
    _description = "Location Conf"
    _rec_name = 'city'


    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country')
    image = fields.Binary(string="Image")

    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        return country

    country_id = fields.Many2one('res.country', default=_get_default_country)

