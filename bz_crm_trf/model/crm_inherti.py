# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class TrfFrom(models.Model):
    _inherit = ["crm.lead"]

    trf_view_id = fields.Many2one("trf", string="TRF View")
    trf_count = fields.Integer('# Scope Matrix', compute='_compute_trf_count')

    def _compute_trf_count(self):
        if self.ids:
            scope_data = self.env['trf'].sudo().read_group([
                ('crm_id', 'in', self.ids)
            ], ['crm_id'], ['crm_id'])
            mapped_data = {m['crm_id'][0]: m['crm_id_count'] for m in scope_data}
        else:
            mapped_data = dict()
        for scope in self:
            scope.trf_count = mapped_data.get(scope.id, 0)

    @api.model
    def create(self, vals):
        res = super(TrfFrom, self).create(vals)
        if self.env.context.get('active_id'):
            ggg = self.env.context.get('active_id')
            res.trf_view_id = ggg
        return res


    def action_trf_form_new(self):
        ctx = {
            'default_name': self.partner_name,
            'default_contact_persons_name': self.partner_id.id,
            'default_contact_person_Designation': self.function,
            'default_contact_persons_phone_number': self.phone,
            'default_email': self.email_from,
            'default_street': self.street,
            'default_street2': self.street2,
            'default_zip': self.zip,
            'default_city': self.city,
            'default_state_id': self.state_id.id,
            'default_country': self.country_id.id,
            'default_user_id': self.user_id.id,
            'active_id': self.id
        }
        print(self.partner_id.id)
        return {
            "name": _("TRF"),
            "view_mode": "form",
            "res_model": "trf",
            "type": "ir.actions.act_window",
            'context': ctx,
        }


    def action_trf_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "TRF",
            "res_model": "trf",
            "domain": [("crm_id", "=", self.id)],
            "view_mode": "tree,form",
            'target': 'current',
        }


class ProposalInherite(models.Model):
    _inherit = ["sale.order"]

    contact_person = fields.Many2one('res.partner', string='Contact Person')
    bank = fields.Char(string='Bank Name')
    account_no = fields.Integer(string="A/c No.")
    ifsc = fields.Char(string='IFSC')
    word_num = fields.Char(string="Amount In Words:", compute='_amount_in_word')

    def _amount_in_word(self):
        for rec in self:
            rec.word_num = str(rec.currency_id.amount_to_text(rec.amount_total))

