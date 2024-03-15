from odoo import api, fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    presenter = fields.Many2one('res.partner', string='Presenter')
    facilitator = fields.Many2one('res.partner', string='Facilitator')
    note_taker = fields.Many2one('res.partner', string='Note Taker')
    time_keeper = fields.Many2one('res.partner', string='Time Keeper')
    agenda_items = fields.Text(string='Agenda Items')
    action_items = fields.Text(string='Action Items')
    conclusion = fields.Text(string='Conclusion')




