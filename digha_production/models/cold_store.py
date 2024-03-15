# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError


class ColdStore(models.Model):
    _name = 'cold.store'

    company = fields.Char(string="Company")
    unit = fields.Char(string="Unit")
    cold_store_date = fields.Date(string="Cold Store Date")
    cold_store_supervisor = fields.Char(string='Cold Store Supervisor')
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

    cold_store_details_ids = fields.One2many('coldstore.details', 'cold_store_details_id', string="cold store details ids", invisible=True)


class ColdStoreDetails(models.Model):
    _name = 'coldstore.details'

    lot_number = fields.Many2one('stock.production.lot', string="Lot No")
    product_id = fields.Many2one('product.product', string="Product")
    cooking = fields.Char(string='Cooking')
    freezing = fields.Char(string='Freezing')
    brand = fields.Char(string='Brand')
    glaze = fields.Char(string='Glaze')
    pack_by = fields.Char(string="Pack By")
    packing_style = fields.Char(string="Packing Style")
    store_location = fields.Char(string="Store Location")
    rack_pallet = fields.Char(string="Rack/Pallet")
    available_capacity = fields.Char(string="Available Capacity(kgs)")
    no_of_mc = fields.Char(string="No Of M/C")
    loose = fields.Char(string="Loose")
    place_qty = fields.Char(string="Place Qty")
    po_no = fields.Char(string="PO NO")
    remark = fields.Char(string="Remarks")

    cold_store_details_id = fields.Many2one('cold.store', string="Cold Store Details id", invisible=True)

