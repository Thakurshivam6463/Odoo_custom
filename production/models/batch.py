# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FishDeHeading(models.Model):
    _name = 'fish.de_heading'
    _rec_name = 'vendor_id'

    batch_id = fields.Many2one('fish.batch', 'Batch')
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    man_power = fields.Float('No. of Man Power')
    material = fields.Float("Material in KG")
    received_material = fields.Float('Received Material in KG')
    average_per_man = fields.Float('Average Per Man')
    spend_time = fields.Float('Spend Time')


class FishBatch(models.Model):
    _name = 'fish.batch'
    _rec_name = 'name'

    name = fields.Char("Batch Name", default=lambda self: self.env['ir.sequence'].next_by_code('fish.batch'))
    batch_date = fields.Date("Batch Date")
    status = fields.Selection(
        [('draft', 'Draft'), ('verifying', 'Verifying'), ('complete', 'Complete'),
        ], default='draft', string="Stage")
    deheading_ids = fields.One2many('fish.de_heading', 'batch_id', 'De-Heading')
    receiving_id = fields.Many2one('materials.reciving.deck', 'Receiving')

    @api.model
    def create(self, values):
        print(values)
        receiving_id = self.env['materials.reciving.deck'].sudo().browse(self.env.context.get('active_id'))
        values.update({'receiving_id' : self.env.context.get('active_id')})
        res = super(FishBatch,self).create(values)
        if res:
            receiving_id.write({'batch_id':res.id})
        return res



