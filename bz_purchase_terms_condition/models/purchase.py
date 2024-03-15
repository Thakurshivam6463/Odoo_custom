from odoo import fields, models, api


class Purchase(models.Model):
    _inherit = 'purchase.order'

    terms_id = fields.Many2one('purchase.term.condition', string='Terms & Conditions')

    @api.onchange('terms_id')
    def onchange_term_condition(self):
        if self.terms_id:
            self.notes = self.terms_id.terms
        else:
            self.notes = False