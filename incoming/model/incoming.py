# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectIncomingView(models.Model):
    _inherit = "project.project"

    # sample incoming
    test_request_no = fields.Char(string="Test Request No.")
    time_of_receiving = fields.Datetime(string="DateTime Of Receiving")
    date_of_unpacking = fields.Datetime(string="Date Of Unpacking")
    no_of_samples_ordered = fields.Integer(string="No. of Samples Ordered")
    number_of_samples_received = fields.Integer(string="Number of Samples Received")
    cell_material = fields.Char(string="Cell Material:")
    model_type = fields.Char(string="Model Type:")
    no_of_cells = fields.Char(string="No. of Cells:")
    manufacturer = fields.Char(string="Manufacturer")
    
    l_no = fields.Char(string="ULR No")
    testing = fields.Char(string="Title of Test Report")
    tes = fields.Char(string="")
    
    @api.model
    def create(self, vals):
        if not vals.get('testing'):
            vals['testing'] = 'Test Report'
        res = super(ProjectIncomingView, self).create(vals)
        return res





