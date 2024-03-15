# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class LoadUnload(models.Model):
    _name = 'load.unload'

    company = fields.Char(string="Company")
    unit = fields.Char(string="Unit")
    production_date = fields.Date(string="Production Date")
    freezer = fields.Many2one('freezer', string="Freezer")
    load_number = fields.Char(string="Load No")
    loading_time = fields.Many2one('start.time', string="Loading Time")
    store_supervisor = fields.Many2one('hr.employee', string='Store Supervisor')
    packing_date = fields.Date(string='Packing Date')
    feeding_end = fields.Many2one('start.time', string='Feeding End')
    production_supervisor = fields.Many2one('hr.employee', string="Production Supervisor")
    system_rec_no = fields.Char(string="System Rec No")
    create_date = fields.Char(string="Create Date")
    notes = fields.Char(string="Notes")
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submit'), ('complete', 'Complete'), ('verified', 'Verified'),
         ('cancel', 'Cancel'), ],
        default='draft', string="Status")

    def action_draft(self):
        self.state = 'draft'

    def action_submit(self):
        self.state = 'submit'

    def action_complete(self):
        self.state = 'complete'

    def action_verified(self):
        self.state = 'verified'

    def action_cancel(self):
        self.state = 'cancel'


    production_details_ids = fields.One2many('production.details', 'production_details_id',string="production details ids", invisible=True)


class ProductionDetails(models.Model):
    _name = 'production.details'

    pre_processed = fields.Boolean(string="Pre Processed")
    value_added = fields.Boolean(string="Value Added")
    lot_number = fields.Many2one('stock.production.lot', string="Lot No")
    variety = fields.Char(string="Variety")
    available_qty = fields.Char(string="Available Qty")
    product_id = fields.Many2one('product.product', string="Product")
    cooking = fields.Char(string='Cooking')
    brand = fields.Char(string='Brand')
    glaze = fields.Char(string='Glaze')
    packing_type = fields.Char(string="Packing Type")
    pack_by = fields.Char(string="Pack By")
    packing_slab = fields.Char(string="Packing Slab")
    packing_style = fields.Char(string="Packing Style")
    feed_qty = fields.Char(string="Feed Qty")
    no_of_mc = fields.Char(string="No Of M/C")
    loose_qty = fields.Char(string="Loose Qty")
    previous_loose = fields.Char(string="Previous Loose")
    packed_qty = fields.Char(string="Packed Qty")
    notes = fields.Char(string="Notes")

    production_details_id = fields.Many2one('load.unload', string="production details")

