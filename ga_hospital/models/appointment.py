# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointment"
    _order = "doctor_id,name,age"

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self:_('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_name_id = fields.Many2one('hospital.patient', string='Patient Name', required=False)
    age = fields.Integer(string='Age', related='patient_id.age', tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor",required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], default='draft', string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible")
    note = fields.Text(string='Description')
    date_appointment = fields.Date(string="Date")
    date_checkup = fields.Datetime(string="Check up time")
    prescription = fields.Text(string="Prescription")
    prescription_line_ids = fields.One2many('appointment.prescription.line', 'appointment_id', string="Prescription Line")

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        if vals.get('name', _('New')) == _('New'):
           vals['name'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    # To Add Onchange Function in Odoo
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''

    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("You cannot delete %s as it is in done State" % self.name))
        return super(HospitalAppointment, self).unlink()

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'http://localhost:8069/web#id=421&action=35&model=ir.module.module&view_type=form&cids=&menu_id=5'
        }


class AppointmentPrescriptionLine(models.Model):
    _name = "appointment.prescription.line"
    _description = "Appointment Prescription Line"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
