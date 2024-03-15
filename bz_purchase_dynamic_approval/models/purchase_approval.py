# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

from odoo import fields, models


class PurchaseApproval(models.Model):
    _name = 'purchase.approval'
    _description = 'Purchase Dynamic Approval Configuration'

    company_id = fields.Many2one('res.company', string='Company')
    from_amount = fields.Float(string='From Amount')
    to_amount = fields.Float(string='To Amount')
    process_by = fields.Selection(string='Approve Process By',
                                  selection=[('users', 'Users'),
                                             ('groups', 'Groups')],
                                  default='users', required=True)
    user_ids = fields.Many2many('res.users', string='Users')
    group_ids = fields.Many2many('res.groups', string='Groups')