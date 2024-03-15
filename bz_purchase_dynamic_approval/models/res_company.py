# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    purchase_dynamic_approval_ids = fields.One2many('purchase.approval', 'company_id', string='Dynamic Sale Approval')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
