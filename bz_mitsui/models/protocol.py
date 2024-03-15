# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProtocolForm(models.Model):
    _inherit = "protocol.form"
    _rec_name = 'process_type_id'

    parameter_ids = fields.One2many('protocol.line', 'parameter', string='Parameter')
    equipment_list_ids = fields.One2many('equipment.detail','equipment_list_id',string="Equipment List ids", invisible=True)
    standard_id = fields.Many2one('standards', string='Standard')
    process_type_id = fields.Many2one('process.type', string='Test Type')
    ambient_temperature = fields.Char(string="Ambient Temperature")
    humidity = fields.Char(string="Humidity")
    remarks = fields.Text(string='Remarks')

class ProtocolLine(models.Model):
    _name = "protocol.line"

    parameter_id = fields.Many2one('protocol.parameter', string='Parameter')
    value = fields.Char(string='Parameter Value')
    parameter = fields.Many2one('protocol.form', string='Parameter')
    
class  EquipmentListForm(models.Model):
    _name = "equipment.detail"
    _description = " Equipment From"

    equipment_name = fields.Many2one('maintenance.equipment',string="Equipment Name")
    equipment_id = fields.Char(string="Equipment ID")
    calibration_due_date = fields.Date(string="Calibration due Date")

    equipment_list_id = fields.Many2one('protocol.form',string="Equipment List Id", invisible=True)


    @api.onchange('equipment_name')
    def onchange_equipment_name_details(self):
        if self.equipment_name:
            self.calibration_due_date = self.equipment_name.calibration_due_date
            self.equipment_id = self.equipment_name.equipment_id









