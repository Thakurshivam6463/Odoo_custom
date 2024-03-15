# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

from odoo import models, fields, _
from odoo.exceptions import UserError


class Sale(models.Model):
    _inherit = 'sale.order'

    def compute_is_dynamic_approver(self):
        for rec in self:
            approver = False
            authorized_users = []
            approval_id = self.env['sale.approval'].search([('from_amount', '<=', rec.amount_total),
                                                            ('to_amount', '>=', rec.amount_total),
                                                            ('company_id', '=', rec.company_id.id)], limit=1)
            if approval_id:
                if approval_id.process_by == 'users':
                    for user in approval_id.user_ids:
                        if user.id not in authorized_users:
                            authorized_users.append(user.id)
                if approval_id.process_by == 'groups':
                    for group in approval_id.group_ids:
                        if group.users:
                            for user in group.users:
                                if user.id not in authorized_users:
                                    authorized_users.append(user.id)
            if rec.env.user.id in authorized_users:
                approver = True
            rec.is_dynamic_approver = approver

    def action_confirm(self):
        if self.company_id and self.company_id.sale_dynamic_approval_ids:
            approval_id = self.env['sale.approval'].search([('from_amount', '<=', self.amount_total),
                                                            ('to_amount', '>=', self.amount_total),
                                                            ('company_id', '=', self.company_id.id)], limit=1)
            if approval_id:
                self.state = 'dynamic_approval'
            else:
                super(Sale, self).action_confirm()
        else:
            super(Sale, self).action_confirm()

    def dynamic_approval(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write(self._prepare_confirmation_values())
        self._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('dynamic_approval', 'To Approve'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    is_dynamic_approver = fields.Boolean(string='Dynamic Approver', compute='compute_is_dynamic_approver')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
