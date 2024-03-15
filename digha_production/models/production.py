# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class FishProductions(models.Model):
    _name = 'fish.production'
    _rec_name = 'lot_number'

    lot_number = fields.Many2one('stock.production.lot', string="Lot No")
    processing_unit = fields.Char(string="Processing Unit")
    date = fields.Date(string="Date")
    time = fields.Many2one('start.time', string="Time")
    start_date_time = fields.Char(string="Start Date Time")
    note = fields.Char(string="Note")
    process_at = fields.Selection(selection=[('in house', 'In House'), ('third party', 'Third Party'), ], string='Process AT', default='in house')
    shift = fields.Selection(selection=[('morning', 'Morning'), ('noon', 'Noon'), ('evening', 'Evening'), ], string='Shift')
    supervisor = fields.Many2one('hr.employee', string="Supervisor")


    product_ids = fields.One2many('sea.food', 'production_id', string="product ids", invisible=True)
    grading_details_ids = fields.One2many('grading.detail', 'grading_details_id', string="grading details ids", invisible=True)

    soak_count = fields.Integer('# Soak Out', compute='_compute_soak_count')

    def _compute_soak_count(self):
        if self.ids:
            soak_data = self.env['soak.out'].sudo().read_group([
                ('soak_id', 'in', self.ids)
            ], ['soak_id'], ['soak_id'])
            mapped_data = {m['soak_id'][0]: m['soak_id_count'] for m in soak_data}
        else:
            mapped_data = dict()
        for soak in self:
            soak.soak_count = mapped_data.get(soak.id, 0)

    @api.onchange('lot_number')
    def onchange_lot_number(self):
        if self.lot_number:
            self.date = self.lot_number.create_date
            self.product_ids = [
                (0, 0, {
                    'product_id': self.lot_number.product_id.id,
                    'qty': self.lot_number.product_qty,
                    'batch_date': self.lot_number.create_date
                })
            ]

    def action_soak_out_form(self):
        return {
            "name": _("Soak Out"),
            "view_mode": "form",
            "res_model": "soak.out",
            "type": "ir.actions.act_window",
            # 'context': {'active_id': self.id, 'ref': self.reference},
            # "domain": [("id", "in", result_list)],
        }

    def action_soak_out_view(self):
        return {
            'type': "ir.actions.act_window",
            'name': 'Soak Out',
            "res_model": "soak.out",
            "domain": [("soak_id", "=", self.id)],
            "view_mode": "tree,form",
            'target': 'current',
        }

class ProductionId(models.Model):
    _name = 'sea.food'

    production_id = fields.Many2one('fish.production', string="Production", invisible=True)

    product_id = fields.Many2one('product.product', string="Product")
    process_type = fields.Char(string="Process Type")
    batch_date = fields.Date(string="Batch date")
    status = fields.Char(string="Status")
    qty = fields.Float(string="Quantity")
    batch = fields.Char(string="Batch")

    # @api.onchange('lot_number')
    # def onchange_lot_number(self):
    #     line_val = []
    #     for line in self.project_id.product_ids:
    #         line_val.append((0, 0, {'product_id': line.product_id.id,
    #                                 'source_location': line.source_location.id,
    #                                 # 'destination_location': line.destination_location.id,
    #                                 'qty': line.qty
    #                                 }))
    #     ctx = {
    #         'default_sample_line_ids': line_val
    #     }

class GradingDetails(models.Model):
    _name = 'grading.detail'

    grading_details_id = fields.Many2one('fish.production', string="Grading Details", invisible=True)

    preprocessed_product = fields.Many2one('product.product', string="Preprocessed Product")
    grade = fields.Many2one('grade.count', string="Grade Count")
    value_add_product = fields.Many2one('valueadd.product',string="Value Add Product")
    waste_qty = fields.Char(string="Waste Quantity")
    quantity = fields.Float(string="Quantity")
    yield1 = fields.Char(string="Yield")
    socking = fields.Boolean(string="Socking")
    remarks = fields.Text(string="Remarks")
