from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def default_get(self, fields):
        if self.env.context.get('default_so_id'):
            self = self.with_context(
                default_res_model_id=self.env.ref('sale.model_sale_order').id,
                default_res_id=self.env.context['default_so_id']
            )
        defaults = super(CalendarEvent, self).default_get(fields)
        return defaults

    so_id = fields.Many2one(
        'sale.order', 'Sale order', index=True, ondelete='set null')


