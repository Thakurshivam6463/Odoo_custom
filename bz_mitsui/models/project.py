# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _
import datetime
from odoo.exceptions import ValidationError

class Project(models.Model):
    _inherit = 'project.project'

    ulr = fields.Char(string='ULR')
    title = fields.Char(string="Title of Test Report")

    ilac_logo = fields.Boolean(string="ilac Logo")
    tc = fields.Boolean(string="NABL Logo")
    pi = fields.Boolean(string="Technical Licensing Partner")
    attachment = fields.Many2many('ir.attachment',  string='Attachments', )

    prepared_by = fields.Binary(string='Signature')
    prepared_by_name = fields.Char(string="Prepared By")
    authorized_by = fields.Binary(string='Signature')
    authorized_by_name = fields.Char(string="Authorized By")
    verified_by = fields.Binary(string='Signature ')
    verified_by_name = fields.Char(string="Verified By")
    issued_by = fields.Binary(string=' Signature')
    issued_by_name = fields.Char(string="Issued By")
    

    # @api.model
    # def create(self, vals):
    #     if not vals.get('title'):
    #          vals['title'] = 'Test Report'
    #     res = super(Project, self).create(vals)
    #     return res



class FlowChartImage(models.Model):
    _inherit = ["project.task"]

    attachment = fields.Binary(string='Flow Chart Image')
    abbreviations_id = fields.Many2one('abbreviations',string="Abbreviation")
    protocol_id = fields.Many2one('protocol.form',string="Protocol")
    result_compilation = fields.Html(string='Result Compilation')


