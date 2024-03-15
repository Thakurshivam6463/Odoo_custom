# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Species(models.Model):
    _name = 'species.species'
    _rec_name = 'name'
    _description = 'Species'

    name = fields.Char('Name')


class Count(models.Model):
    _name = 'count.count'
    _rec_name = 'name'
    _description = 'Count'

    name = fields.Char('Name')


class GateEntry(models.Model):
    _name = 'new.gate.entry'
    _rec_name = 'gate_paas_number'
    _description = 'Gate Entry'

    @api.depends('materials_carates', 'ice_carates', 'empty_carates')
    def _cal_total_carates(self):
        for rec in self:
            rec.total_carates = rec.materials_carates + rec.ice_carates + rec.empty_carates

    gate_paas_number = fields.Char('Gate Pass Number', readonly=True)
    supplier_id = fields.Many2one('res.partner', 'Supplier', required=True)
    rec_type = fields.Char('Type', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    vehicle_number = fields.Char(string='Vehicle Number', required=True)
    driver_mobile_number = fields.Char(string='Driver Mobile Number', required=True)
    materials_carates = fields.Integer(string='Material Crates', required=True)
    ice_carates = fields.Integer(string='Ice Crates', required=True)
    empty_carates = fields.Integer(string='Empty Crates', required=True)
    total_carates = fields.Integer(compute='_cal_total_carates', string='Total Crates', required=True)
    driver_id = fields.Many2one('res.partner', 'Driver Name', required=True)
    entry_date = fields.Datetime('Entry Datetime', required=True, default=fields.Datetime.now())
    seal_no = fields.Char(string='Seal No.')
    supervisor_name = fields.Many2one('res.partner', 'Grader/Supervisor Name')
    rec_from = fields.Char(string='From')
    rec_state = fields.Char(string='State')
    material_details_ids = fields.One2many('material.details', 'gate_entry_id', required=True)
    status = fields.Selection([('draft', 'Draft'), ('batch_code_generated', 'Batch Code Generate')], default='draft', string="Stage")

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.vehicle_number = self.vehicle_id.vin_sn
            if self.vehicle_id.driver_id:
                self.driver_id = self.vehicle_id.driver_id

    def generate_gate_pass(self):
        self.gate_paas_number = self.env['ir.sequence'].next_by_code('new.gate.entry')
        self.status = 'batch_code_generated'

class MaterialDetails(models.Model):
    _name = 'material.details'
    _rec_name = 'species_id'
    _description = 'Material Details'

    species_id = fields.Many2one("species.species", string="Particulars")
    grams = fields.Float(string="Grams")
    weight = fields.Float(string="Weight")
    grade_id = fields.Many2one("grade.grade", string="Grade")
    count_id = fields.Many2one("count.count", string="Count")
    count = fields.Integer(string="Count")
    quality_inspections = fields.Char(string="Quality Inspections")
    photos = fields.Binary(string="Photos")
    no_of_carates = fields.Integer(string="No. of Crates")
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    gate_entry_id = fields.Many2one('new.gate.entry', string='Gate Entry')
