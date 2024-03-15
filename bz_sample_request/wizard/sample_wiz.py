# -*- coding: utf-8 -*-
from odoo import api, fields, models


class WizardSampleMove(models.TransientModel):
    _name = "wizard.sample.move"
    _description = "Wizard Sample Move"

    sample_line_ids = fields.One2many('wizard.sample.move.line', 'sample_line_id', string="Sample lines", invisible=True)
    sm_in = fields.Many2one('project.task', string="ABC")

    def action_sample_apply(self):
        active_id = self.env.context.get('active_id')
        line_val = []
        picking_type = self.env['stock.picking.type'].search([('name', '=', 'Internal Transfers')])
        if picking_type:
            picking_id = picking_type
        for line in self.sample_line_ids:
            line_val.append((0, 0,{'product_id': line.product_id.id,
                                   'source_location': line.source_location.id,
                                   'destination_location': line.destination_location.id,
                                   'qty': line.qty
                                   }))
            move = self.env['stock.move'].create({
                'name': 'Use on MyLocation',
                'location_id': line.source_location.id,
                'location_dest_id': line.destination_location.id,
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.qty,
            })
            move._action_confirm()
            move._action_assign()
            move.move_line_ids.write(
                {'qty_done': line.qty,
                 'location_id': line.source_location.id,
                 'location_dest_id': line.destination_location.id
                 })
            move._action_done()
        if active_id:
            task = self.env['project.task'].browse(active_id)
            project = task.project_id.product_ids = line_val




class WizardSampleMoveLine(models.TransientModel):
    _name = "wizard.sample.move.line"
    _description = "Wizard Sample Move Line"

    product_id = fields.Many2one('product.product', string="Product  ")
    source_location = fields.Many2one('stock.location', string="Source Location ")
    destination_location = fields.Many2one('stock.location', string='Destination Location')
    qty = fields.Float(string='Quantity')

    sample_line_id = fields.Many2one('wizard.sample.move', string="Line", invisible=True)












