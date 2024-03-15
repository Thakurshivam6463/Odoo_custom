# -*- coding: utf-8 -*-

from odoo import models, fields, api

class GstNumber(models.Model):
    """ Add gst Numbers """
    _name = 'gst.number'
    _description = 'Gst Number'
    _order = 'sequence, id'

    name = fields.Char('GST Number')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    partner_id = fields.Many2one('res.partner',string="Customer")
    sequence = fields.Integer(default=10)

class CustomResPartner(models.Model):
    """ Add gst Number """
    _inherit = 'res.partner'
    _description = 'Add gst Number'

    partner_gst_number = fields.Char('GSTIN Number')
    gst_number_ids = fields.One2many('gst.number', 'partner_id', string="GST Number")
    # vat = fields.Char(string="GST number", compute='_compute_vat', store=True)

    # @api.depends('gst_number_ids')
    # def _compute_vat(self):
    #     for rec in self:
    #         rec.vat = "AB102030405578"

    @api.onchange('gst_number_ids','gst_number_ids.name', 'gst_number_ids.from_date', 'gst_number_ids.to_date')
    def gst_number_ids_change(self):
        for rec in self:
            if rec.gst_number_ids:
                vat = rec.gst_number_ids[-1].name
                rec.vat = vat
                if len(vat) >= 12:
                    rec.ipanno = rec.vat[2:12]
                # else:
                #     rec.ipanno = False
            # else:
            #     rec.vat = False
            #     rec.ipanno = False

    def write(self, vals):
        rec = super(CustomResPartner, self).write(vals)
        # print("===========WRITE=====", rec,vals)
        if self.gst_number_ids:
            vat = self.gst_number_ids[-1].name
            if self.vat != vat:
                # print("======IF======VAT=====WRITE===1==",vat)
                self.write({
                    'vat':vat,
                })
            if len(vat) >= 12 and self.ipanno != vat[2:12]:
                # print("======IF======VAT=====WRITE===2==", vat)
                self.write({
                    'ipanno': vat[2:12]
                })
        return rec



class ResPartnerBank(models.Model):
    """ Add gst Number """
    _inherit = 'res.partner.bank'
    _description = 'Add IFSC Code'

    ifsc_code = fields.Char('IFSC Code')