from odoo import models, fields, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    meeting_count = fields.Integer('# Meetings', compute='_compute_meeting_count')

    def _compute_meeting_count(self):
        if self.ids:
            meeting_data = self.env['calendar.event'].sudo().read_group([
                ('so_id', 'in', self.ids)
            ], ['so_id'], ['so_id'])
            mapped_data = {m['so_id'][0]: m['so_id_count'] for m in meeting_data}
        else:
            mapped_data = dict()
        for sale in self:
            sale.meeting_count = mapped_data.get(sale.id, 0)

    def action_schedule_meeting(self):
        """ Open meeting's calendar view to schedule meeting on current Sale Order.
            :return dict: dictionary value for created Meeting view
        """
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")
        partner_ids = self.env.user.partner_id.ids
        ctx = {
            'default_partner_id': self.partner_id.id,
            'default_so_id': self.id,
            'default_partner_ids': partner_ids,
            'default_attendee_ids': [(0, 0, {'partner_id': pid}) for pid in partner_ids],
            'default_team_id': self.team_id.id,
            'default_name': self.name,
        }
        return {
            "name": _("Sale Meeting"),
            "view_mode": "form",
            "res_model": "calendar.event",
            "type": "ir.actions.act_window",
            'context': ctx,
        }

    def action_view_meeting(self):
        return {
            "name": _("Sale Meeting"),
            "view_mode": "calendar",
            "res_model": "calendar.event",
            "type": "ir.actions.act_window",
            'domain': [('so_id', 'in', self.ids)]
        }