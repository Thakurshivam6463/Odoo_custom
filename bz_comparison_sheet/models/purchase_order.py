# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################
import base64
from io import BytesIO

from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.misc import xlwt
from xlwt import easyxf


class purchase_order(models.Model):
    _inherit = 'purchase.order'

    performance = fields.Char(string = 'Performance')
    credentials = fields.Char(string = 'Credentials')  
    commercial_rating = fields.Char(string ='Commercial Rating')
    technical_rating  = fields.Char(string = 'Technical Rating')
    final_recommendtation  = fields.Char(string = 'Final Recommendtation')
    any_other  = fields.Char(string = 'Any Other')
    delivery = fields.Char(string = 'Delivery') 
    ld_clause = fields.Char(string = 'LD Clause')
    warranty = fields.Char(string = 'Warranty')
    
    packing_forwarding = fields.Selection([('fixed','Fixed'),('percentage','Percentage')],default='fixed',string = 'Packing & Forwarding')
    packing_forwarding_charges = fields.Float(string = 'Packing & Forwarding Charges')
    
    freight = fields.Selection([('fixed','Fixed'),('percentage','Percentage')],default='fixed',string = 'Freight')
    freight_charges = fields.Float(string = 'Freight Charges')
    
    other = fields.Selection([('fixed','Fixed'),('percentage','Percentage')],default='fixed',string = 'Other Charges')
    other_charges = fields.Float(string = 'Other Charges')
    
    landed_cost_lc = fields.Float(string = 'Landed Cost (LC) in Rs')
    landed_cost_lc_gst = fields.Float(string = 'Landed Cost (LC) net off GST -in Rs')
                    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
