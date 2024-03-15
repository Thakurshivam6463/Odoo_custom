# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime
from odoo.exceptions import ValidationError


class TrfFrom(models.Model):
    _name = "trf"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "TRF From"

    reference = fields.Char(string='Reference No.', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    date = fields.Date(string='Date', default=datetime.date.today())
    doc_no = fields.Char(string="Doc No")
    rev_no = fields.Char(string="Rev No")
    name = fields.Char(string="Customer Name", required=True)
    type = fields.Char(string='type')
    user_id = fields.Many2one('res.users',string="Sales Person")
    address = fields.Char(string='Address of organisation')
    contact_persons_name = fields.Many2one('res.partner', string='Contact persons name', required=True)
    contact_person_Designation = fields.Char(string='Contact Person Designation')
    contact_persons_phone_number = fields.Char(string='Contact Persons Phone Number')
    email = fields.Char(string='E-mail')
    delivery_challan = fields.Boolean(string='Delivery Challan:')
    tranport_intimation = fields.Boolean(string='Tranport intimation:')
    transit_insurance_intimation = fields.Boolean(string='Transit Insurance intimation:')
    drawings_catalogs_operating_manual_provided = fields.Boolean(
         string='Drawings/Catalogs/Operating Manual (Provided):')
    noc_if_not_the_original_manufacture = fields.Boolean(string='NOC if not the original manufacture:')
    type_of_testing_requested = fields.Selection([
        ('evaluation', 'Evaluation'),
        ('development', 'Development'),
    ])
    witnessing_required = fields.Boolean(string='Witnessing Required:')
    test_reports_required_One_for_all_tests = fields.Boolean(string='Test reports required:')
    if_separate_reports_required_for_each_test_sample = fields.Boolean(
        string='If Separate Reports Required For Each Test/Sample:')
    whether_sample_will_be_collected_back = fields.Boolean(string='Whether Sample Will Be Collected Back:')
    requirement_of_statement_of_confirmty = fields.Boolean(string='Requirement of Statement of Confirmty:')
    statement_of_confirmty = fields.Selection([
        ('decision_on_compliance',
         'Decision on Compliance to specification will be based on the tolerance mentioned in the Standard specification'),
        ('for_the_tolerance',
         'For the tolerance specified by the customer, same will be considered for decision criteria_____kindly allow the customer to mention the criteria (Note: Deviations requested by the customer shall not impact the integrity of the laboratory or the validity of the results)'),
        ('if_measurement_uncertainty',
         "If Measurement Uncertainty to be considered for decision on compliance, MCIND's calculated Measurement Uncertainty at confidence level of approximately 95% will be acceptable"),
    ])
    document_details_ids = fields.One2many('document.details', 'trf_id', string="Sample & Document Details")
    sample_quantity_received = fields.Char(string="Sample Quantity Received:")
    samples_received_in_good_condition = fields.Boolean(string="Samples received in good condition:")
    test_method_competency_available = fields.Boolean(string="Test Method Competency available:")
    if_no_does_the_completion_requires_sub_contracting = fields.Boolean(string="If no does the completion requires sub-contracting:")
    report_duration_feasible = fields.Boolean(string="Report Duration Feasible:")
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state', 'Fed. State', domain="[('country_id', '=?', country)]")
    country = fields.Many2one('res.country')
    state = fields.Selection(
        [('draft','Draft'),('sales_pic', 'Sales PIC'), ('technical_manager', 'Technical manager'), ('technical_head', 'Technical head'), ('lab_manager', 'Lab Manager'),
         ('reject', 'Rejected')],
        default='draft', string="Status", tracking=True)
    crm_id = fields.Many2one("crm.lead", string="CRM View")

    scope_count = fields.Integer('# Scope Matrix', compute='_compute_scope_count')

    def _compute_scope_count(self):
        if self.ids:
            scope_data = self.env['scope.matrix'].sudo().read_group([
                ('trf_id', 'in', self.ids)
            ], ['trf_id'], ['trf_id'])
            mapped_data = {m['trf_id'][0]: m['trf_id_count'] for m in scope_data}
        else:
            mapped_data = dict()
        for scope in self:
            scope.scope_count = mapped_data.get(scope.id, 0)


    
    def action_sales_pic(self):
        self.state = 'sales_pic'

    def action_technical_manager(self):
        if self.env.user.has_group('bz_crm_trf.group_trf_pic_user'):
            self.state = 'technical_manager'
        else:
            raise ValidationError(
                _(
                    "Only Sales PIC can approved this."
                )
            )


    def action_technical_head(self):
        if self.env.user.has_group('bz_crm_trf.group_trf_pic_user'):
            self.state = 'technical_head'
        else:
            raise ValidationError(
                _(
                    "Only Technical Manager can approved this."
                )
            )

    def action_lab_manager(self):
        if self.env.user.has_group('bz_crm_trf.group_trf_pic_user'):
            self.state = 'lab_manager'
        else:
            raise ValidationError(
                _(
                    "Only Technical Head can approved this."
                )
            )

    def action_reject(self):
        self.state = 'reject'



    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('trf') or _('New')
        res = super(TrfFrom, self).create(vals)
        if self.env.context.get('active_id'):
            vvv = self.env.context.get('active_id')
            res.crm_id = vvv
        return res

    def action_scope_matrix_form(self):
        line = []
        if self.document_details_ids:
            for req in self.document_details_ids:
                line.append((0, 0, {
                    'product_id': req.product_no.id,
                    'test_description': req.sample_specifications,
                    'quantity': req.no_of_sample,
                    'standard_id': req.standard_id.id,
                }))
        ctx = {
            'default_trf_reference': self.reference,
            # 'default_standard_id': self.standard_id.id,
            'default_assign_user': self.user_id.id,
            'active_id': self.id,
            'default_batch_scope_matrix_ids': line
        }
        return {
            "name": _("Scope Matrix"),
            "view_mode": "form",
            "res_model": "scope.matrix",
            "type": "ir.actions.act_window",
            'context': ctx,
            # 'context': {'active_id': self.id, 'ref': self.reference},
            # "domain": [("id", "in", result_list)],
        }




    def action_scope_view(self):
        return {
            'type': "ir.actions.act_window",
            'name' : 'Scope Martrix',
            "res_model": "scope.matrix",
            "domain": [("trf_id", "=", self.id)],
            "view_mode": "tree,form",
            'target': 'current',
        }

        # scope_data = self.env['trf'].search([]).ids
        # return {
        #     "name": _("Scope Matrix"),
        #     "view_mode": "tree,form",
        #     "res_model": "scope.matrix",
        #     "type": "ir.actions.act_window",
        #     "domain": [("id", "in", scope_data)]
        # }

    # @api.onchange('name')
    # def onchange_total_project_time(self):
    #    if self.name:
    #        self.street = self.name.street
    #        self.street2 = self.name.street2
    #        self.zip = self.name.zip
    #        self.city = self.name.city
    #        self.state_id = self.name.state_id
    #        self.country = self.name.country_id


class DocumentDetails(models.Model):
    _name = "document.details"
    _description = "Document Details"


    product_no = fields.Many2one('product.product',
                                 string='Identification test samples', required=True)
    product_category = fields.Char(string='Test Requirement:')
    sample_specifications = fields.Char(string="Sample Specifications:")
    system_voltage = fields.Char(string="System Voltage")
    sample_dimensions = fields.Char(string="Sample Dimensions(mm):")
    sample_technology = fields.Char(string="Sample Technology:")
    sample_type = fields.Char(string="Sample Type:")
    no_of_sample = fields.Integer(string='No. Of Samples:')
    connectors_type_and_availability = fields.Char(string="Connectors Availability And Types:")
    decision_rule_agreed_with_customer = fields.Char(string="Decision rule agreed with customer:")
    make = fields.Char(string="Name of Sample Manufacturing Company:")
    Standard_to_be_followed = fields.Char(string="Standard to be Followed:")
    year_of_make = fields.Selection(
        [('2015', '2015'), ('2016', '2016'), ('2017', '2017'),
         ('2018', '2018'),('2019', '2019'), ('2020', '2020'), ('2021', '2021'),('2022', '2022'), ('2023', '2023'), ('2024', '2024'),('2025', '2025'),('2026', '2026'),
         ('2027', '2027'),('2028', '2028'),('2029', '2029'),('2030', '2030'),('2031', '2031'),('2032', '2032'),('2033', '2033'),('2034', '2034'),('2035', '2035'),('2036', '2036'),
         ('2037', '2037'),('2038', '2038'),('2039', '2039'),('2040', '2040'),('2041', '2041'),('2042', '2042'),('2043', '2043'),
         ('2044', '2044'),('2045', '2045'),],
        default='2015', string="Year Of Make", tracking=True)


    trf_id = fields.Many2one('trf', string="Part 2 Sample & Document Details")

    @api.onchange('product_no')
    def onchange_product_details(self):
        if self.product_no:
            self.product_category = self.product_no.categ_id.name
            self.sample_specifications = self.product_no.name
