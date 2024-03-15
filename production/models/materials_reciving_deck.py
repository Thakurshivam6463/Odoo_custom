# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from statistics import mean

def Average(l): 
    avg = mean(l) 
    return avg

class MaterialsQualityGrade(models.Model):
    _name = 'materials.quality.grade'
    _rec_name = 'name'
    _description = 'Materials Quality Grade'

    name = fields.Char(string="Name", required=True)

class MaterialsType(models.Model):
    _name = 'materials.type'
    _rec_name = 'name'
    _description = 'Materials Type'

    name = fields.Char(string="Name", required=True)

class NumberOfCaret(models.Model):
    _name = 'number.of.cartes'
    _rec_name = 'token_genration'
    _description = 'Number Of Caret'

    number_gp = fields.Char(string="Number", required=True)
    supplier_doc = fields.Char(string="Supplier Doc", required=True)
    token_genration = fields.Char(string="Token Genration", required=True)
    real_time_count = fields.Integer(string="Real time count", required=True)
    materials_rec_id = fields.Many2one('materials.reciving.deck', string="Materials Receiving Deck")


class CareteEmptyWeight(models.Model):
    _name = 'carete.empty.weight'
    _rec_name = 'materials_rec_id'
    _description = 'Carete Empty Weight'

    sequence = fields.Integer(string="Sequence", default=1)
    sequence_rel = fields.Integer(string="Sequence No", related='sequence')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    empty_carte_weight = fields.Float(string="Empty Carte Weight", required=True)
    materials_rec_id = fields.Many2one('materials.reciving.deck', string="Materials Receiving Deck")


class MaterialsQuality(models.Model):
    _name = 'materials.quality'
    _rec_name = 'suppier_quality_id'
    _description = 'Materials Quality'

    materials_type = fields.Many2one('materials.type', string="Type", required=True)
    suppier_quality_id = fields.Many2one('materials.quality.grade', string="Suppier Quality", required=True)
    reciving_quality_id = fields.Many2one('materials.quality.grade', string="Receiving Quality", required=True)
    supplier_weight = fields.Float(string='Supplier Weight', required=True)
    received_weight = fields.Float(string='Received Weight', required=True)
    materials_rec_id = fields.Many2one('materials.reciving.deck', string="Materials Receiving Deck")


class MaterialsWeight(models.Model):
    _name = 'materials.weight'
    _rec_name = 'materials_rec_id'
    _description = 'Materials Weight'

    sequence = fields.Integer(string="Sequence", default=1)
    sequence_rel = fields.Integer(string="Sequence No", related='sequence')
    weight = fields.Float(string="Weight", required=True)
    materials_weight = fields.Float(string="Materials Weight", required=True)
    empty_carte_avg_weight = fields.Float(string="Empty Carte Avg Weight")
    materials_rec_id = fields.Many2one('materials.reciving.deck', string="Materials Receiving Deck")
    

class MaterialsRecivingDeck(models.Model):
    _name = 'materials.reciving.deck'
    _rec_name = 'number'
    _description = 'Materials Receiving Deck'

    @api.depends('materials_reciving_time', 'gate_pass_id')
    def _cal_arrival_time_gap(self):
        for rec in self:
            if rec.gate_pass_id:
                import datetime
                data1 = rec.gate_pass_id.entry_date
                data2 = rec.materials_reciving_time
                diff = data2 - data1
                days, seconds = diff.days, diff.seconds
                hours = days * 24 + seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                rec.arrival_time_gap = float(hours)
            else:
                rec.arrival_time_gap = 0.0

    number = fields.Char(string="Number")
    partner_id = fields.Many2one('res.partner', string="Supplier")
    materials_reciving_time = fields.Datetime("Materials Reciving Time", default=fields.Datetime.now)
    arrival_time_gap = fields.Float("Arrival Time Gap(Hours)", compute='_cal_arrival_time_gap')
    gate_pass_id = fields.Many2one('new.gate.entry', string="Gate Pass Number", required=True)
    barcode = fields.Char("Barcode", required=False)
    vehicle_number = fields.Char(string='Vehicle Number')
    date_of_dispatch = fields.Datetime(string='Date of Dispatch', default=fields.Datetime.now())
    number_of_cartes_ids = fields.One2many('number.of.cartes', 'materials_rec_id', string="Number Of Caret")
    carete_empty_weight_ids = fields.One2many('carete.empty.weight', 'materials_rec_id', string="Carete Empty Weight")
    materials_quality_ids = fields.One2many('materials.quality', 'materials_rec_id', string="Materials Quality")
    materials_weight_ids = fields.One2many('materials.weight', 'materials_rec_id', string="Materials Weight")
    lot_number = fields.Char(string="Lot Number")
    status = fields.Selection(
        [('received', 'Materials Receiving Bay'), ('quality', 'Quality'), ('operation', 'Separate Operation'),
         ('complete', ' Receiving Materials Complete'), ('done', 'Batch ID Genrataed')], default='received', string="Stage")
    quality_status = fields.Selection([('g1', 'G1'), ('g2', 'G2'), ('g3', 'G3')], "Quality Grade")
    batch_id = fields.Many2one('fish.batch', 'Batch')
    carete_empty_weight_avg = fields.Float(string="Carete Empty weight Average")

    def action_quality_check(self):
        self.write({'status': 'quality'})

    def action_operation_check(self):
        if not self.batch_id:
            raise UserError(_("First Create Batch from Button Click"))
        self.write({'status': 'operation'})

    def action_complete_received(self):
        self.write({'status': 'complete'})

    def create_batchs(self):
        view_id = self.env.ref('production.fish_batch_form_new').id
        ctx = dict(self.env.context)
        ctx['active_ids'] = self.ids
        return {'type': 'ir.actions.act_window',
                'name': _('Create a Batch'),
                'res_model': 'fish.batch',
                'target': 'new',
                'view_mode': 'form',
                'views': [[view_id, 'form']],

                }

    def batch_id_genrataion(self):
        self.number = self.env['ir.sequence'].next_by_code('materials.reciving.deck')
        self.status = 'done'

    @api.onchange('gate_pass_id')
    def _onchange_gate_pass_id(self):
        if self.gate_pass_id:
            self.vehicle_number = self.gate_pass_id.vehicle_number
            if self.gate_pass_id.supplier_id:
                self.partner_id = self.gate_pass_id.supplier_id.id
            if self.gate_pass_id.material_details_ids:
                weight_final = []
                for line in self.gate_pass_id.material_details_ids:
                    # Create Weight
                    weight_vals = {
                            'uom_id' :line.uom_id.id,
                            'empty_carte_weight' : line.weight,
                            'materials_rec_id' : self.id,
                        }
                    weight_id = self.env['carete.empty.weight'].create(weight_vals)
                    weight_final.append(weight_id.id)
                self.carete_empty_weight_ids = [(6, 0, weight_final)]

    @api.onchange('carete_empty_weight_ids')
    def _onchange_carete_empty_weight_ids(self):
        if self.carete_empty_weight_ids:
            my_list = []
            for rec in self.carete_empty_weight_ids:
                my_list.append(rec.empty_carte_weight)
            self.carete_empty_weight_avg = Average(my_list)

    @api.onchange('materials_weight_ids')
    def _onchange_materials_weight_ids(self):
        if self.materials_weight_ids:
            for rec in self.materials_weight_ids:
                rec.empty_carte_avg_weight = self.carete_empty_weight_avg
                rec.materials_weight = rec.weight - self.carete_empty_weight_avg
