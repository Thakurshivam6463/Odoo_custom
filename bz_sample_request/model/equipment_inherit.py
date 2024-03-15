# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EquipmentinFrom(models.Model):
    _inherit = "maintenance.equipment"

    equi_ids = fields.One2many('equipment.inherit', 'equi', string="Equi", invisible=True)
    equipment_id = fields.Char(string="Equipment ID",required=True, copy=False, readonly=True, default=lambda self: _('New'),)
    calibration_due_date = fields.Date(string="Calibration due Date")

    @api.model
    def create(self, vals):
        if vals.get('equipment_id', _('New')) == _('New'):
            vals['equipment_id'] = self.env['ir.sequence'].next_by_code('maintenance.equipment') or _('New')
        res = super(EquipmentinFrom, self).create(vals)
        return res


class EquipmentFrom(models.Model):
    _name = 'equipment.inherit'

    eq_id = fields.Char(string="EQ ID")
    sensor_device_name = fields.Char(string="Sensor /Device Name")
    type_model = fields.Char(string="Type/Model")
    serial_number = fields.Char(string="Serial Number")
    test_site_location = fields.Char(string="Test site/Location")
    manufacturer = fields.Char(string="Manufacturer")
    calibration_lab = fields.Char(string="Calibration lab")
    calibration_type = fields.Char(string="Calibration Type")
    cal_certificate_no = fields.Char(string="Cal.Certificate No.")
    date_of_calibration = fields.Date(string="Date of calibration")
    next_calibration = fields.Date(string="Next calibration")
    calibrated_range = fields.Char(string="Calibrated Range")
    uncertainty = fields.Char(string="Uncertainty")
    accuracy = fields.Char(string="Accuracy")
    calibration_interval = fields.Char(string="Calibration interval")
    provider = fields.Char(string="Provider")
    traceability = fields.Char(string="Traceability")
    reviewed_by = fields.Char(string="Reviewed by")
    Remarks = fields.Char(string="Remarks")

    equi = fields.Many2one('maintenance.equipment', string="Equi", invisible=True)

