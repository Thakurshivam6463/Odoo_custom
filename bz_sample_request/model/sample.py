# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime
from odoo.http import request
from odoo.exceptions import ValidationError, UserError
from odoo.tools import float_compare, float_is_zero


class SampleRequestForm(models.Model):
    _name = "sample.form"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Sample From"
    _rec_name = 'customer_id'

    customer_id = fields.Many2one('res.partner', string="Customer ", required=1)
    sale_order_id = fields.Many2one('sale.order', string="Sale order", required=1)
    project_id = fields.Many2one('project.project', string=" Project ID", required=1)
    date = fields.Date(string='Date', default=datetime.date.today())
    source_location = fields.Many2one('stock.location', string="Source Location", required=1)
    destination_location = fields.Many2one('stock.location', string='Destination Location', required=1)
    notes = fields.Text(string="Notes")
    sample_request_ids = fields.One2many('sample.request', 'sample_request_id', string="Sample Request", invisible=True, required=1)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancelled')],
        default='draft', string="Status", tracking=True)
    attachment = fields.Binary(string='Delivery Condition image')
    delivery = fields.Selection(
        [('no_physical_damage', 'No Physical Damage'), ('physical_damage', ' Physical Damage'),] ,string="Condition", default='no_physical_damage')
    model = fields.Selection(
        [('good', 'Good'), ('bad', 'Bad')], string="Module", default='good')
    gate = fields.Selection(
        [('gate_no_1', 'Gate No 1'), ('gate_no_2', 'Gate No 2'), ('gate_no_3', 'Gate No 3'), ('gate_no_4', 'Gate No 4')],string="Gate No.", default='gate_no_1')
    test_request_no = fields.Char(string="Test Request No.", readonly=True)
    time_of_receiving = fields.Date(string="Date Of Receiving", default=datetime.date.today())
    date_of_unpacking = fields.Date(string="Date Of Unpacking",default=datetime.date.today())
    no_of_samples_ordered = fields.Integer(string="No. of Samples Ordered")
    number_of_samples_received = fields.Integer(string="Number of Samples Received")
    cell_material = fields.Char(string="Cell Material")
    model_type = fields.Char(string="Model Type")
    sm_id = fields.Many2one("sale.order", string="Sample ")
    move_count = fields.Integer('# Moves', compute='_compute_move_count')
    enable_identical_button = fields.Boolean(string='Identical')
    call_from_identical = fields.Boolean(string='Call from Identical')
    attachment_id = fields.Many2many('ir.attachment',  string='Attachments', )

    #@api.onchange('time_of_receiving', 'date_of_unpacking', )
    #def date_onchange(self):
    #    current_date = datetime.date.today()
    #    for rec in self:
    #        if rec.time_of_receiving > rec.date_of_unpacking:
    #            raise ValidationError(_("Date of Unpacking could not be lower than Date of Receiving"))
    #        if rec.time_of_receiving < current_date:
    #            raise ValidationError(_("Date of Receiving could not be lower than System Date"))



    def action_goahead(self):
        if self.sale_order_id:
            project = self.env['project.project'].search([('sale_order_id', '=', self.sale_order_id.id)])
            if project:
                # template = self.env.ref('bz_sample_request.mail_template_goahead', False)
                mtp = self.env['mail.template']
                ir_model_data = self.env['ir.model.data']
                template_id = ir_model_data.get_object_reference('bz_sample_request',
                                                                 'mail_template_goahead')
                mail_tem = mtp.browse(template_id[1])
                mail_tem.write({'email_to': project.user_id.login})
                mail_tem.send_mail(self.id, True)
                return True

    def _compute_move_count(self):
        if self.ids:
            scope_data = self.env['stock.move'].sudo().read_group([
                ('sample_id', 'in', self.ids)
            ], ['sample_id'], ['sample_id'])
            mapped_data = {m['sample_id'][0]: m['sample_id_count'] for m in scope_data}
        else:
            mapped_data = dict()
        for scope in self:
            scope.move_count = mapped_data.get(scope.id, 0)

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.project_id.sample_id = self.id
        active_id = self.env.context.get('active_id')
        line_val = []
        picking_type = self.env['stock.picking.type'].search([('name', '=', 'Internal Transfers')])
        if picking_type:
            picking_id = picking_type
        for line in self.sample_request_ids:
            line_val.append((0, 0, {'product_id': line.product.id,
                                    'source_location': self.source_location.id,
                                    'destination_location': self.destination_location.id,
                                    'qty': line.qty
                                    }))
            move = self.env['stock.move'].create({
                'name': 'Use on MyLocation',
                'location_id': self.source_location.id,
                'location_dest_id': self.destination_location.id,
                'product_id': line.product.id,
                'product_uom': line.product.uom_id.id,
                'product_uom_qty': line.qty,
                'sample_id': self.id,
            })
            move._action_confirm()
            move._action_assign()
            move.move_line_ids.write(
                {'qty_done': line.qty,
                 'location_id': self.source_location.id,
                 'location_dest_id': self.destination_location.id
                 })
            move._action_done()
        # task = self.env['project.task'].browse(active_id)
        project = self.project_id.product_ids = line_val
            # if move:
            #     self.env['stock.quant']._update_available_quantity(line.product, self.destination_location, line.qty)
        self.state = 'done'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    @api.onchange('customer_id')
    def onchange_sale_order_id(self):
        sale_ids = self.env['sale.order'].search([('partner_id', '=', self.customer_id.id)]).ids
        return {'domain': {'sale_order_id': [('id', 'in', sale_ids)]}}

    @api.onchange('sale_order_id')
    def onchange_project_id(self):
        sale_ids = self.env['project.project'].search([('sale_order_id', '=', self.sale_order_id.id)]).ids
        return {'domain': {'project_id': [('id', 'in', sale_ids)]}}

    def action_move(self):
        return {
            'type': "ir.actions.act_window",
            'name': 'Stock Moves',
            "res_model": "stock.move",
            "domain": [("sample_id", "=", self.id)],
            "view_mode": "tree,form",
            'target': 'current',
        }

    def identical_line(self):
        line_val = []
        if self.sample_request_ids:
            max_id = max(self.sample_request_ids.ids)
            for line in self.sample_request_ids:
                if max_id == line.id:
                    line_val.append((0, 0, {'qty': line.qty,
                    			     'product': line.product.id,
                                            'module_tech': line.module_tech,
                                            'cell_dimension': line.cell_dimension,
                                            'cell_area': line.cell_area,
                                            'module_dimension': line.module_dimension,
                                            'module_area': line.module_area,
                                            'no_of_cells': line.no_of_cells,
                                            'no_of_busbars': line.no_of_busbars,
                                            'connectors_wires_jbox_status': line.connectors_wires_jbox_status,
                                            'module_weight': line.module_weight,
                                            'pmax': line.pmax,
                                            'isc': line.isc,
                                            'voc': line.voc,
                                            'imp': line.imp,
                                            'vmp': line.vmp,
                                            'vmp': line.vmp,
                                            'fuse_rating': line.fuse_rating,
                                            'manufacturer': line.manufacturer,
                                            'year_of_mfg': line.year_of_mfg,
                                            'remarks': line.remarks
                                            }))
            if line_val and self.number_of_samples_received:
                for count in range(self.number_of_samples_received):
                    if count < self.number_of_samples_received - 1:
                        self.sample_request_ids = line_val
                        self.call_from_identical = True



class SampleRequest(models.Model):
    _name = "sample.request"
    _description = "Sample Request"

    product_no = fields.Char(string='Product No')
    product = fields.Many2one('product.product',string='Product Name')
    qty = fields.Float(string='Quantity')
    remarks = fields.Char(string="Remarks")
    sample_no = fields.Char(string="Model No.")
    module_tech = fields.Char(string='Module Technology')
    cell_dimension = fields.Char(string='Cell Dimension(in mm)')
    cell_area = fields.Float(string="Cell Area(in mm SQ)")
    module_dimension = fields.Char(string="Module dimension(in mm)")
    module_area = fields.Float(string="Module Area (in mm sq.)")
    no_of_cells = fields.Integer(string="No. of cells")
    no_of_busbars = fields.Integer(string="No. of Busbars")
    connectors_wires_jbox_status = fields.Char(string="Connectors, Wires & Jbox status")
    module_weight = fields.Float(string="Module weight(kg)")
    manufacturer = fields.Char(string="Manufacturer")
    pmax = fields.Float(string="Pmax (W)")
    isc = fields.Float(string="Isc (A)")
    voc = fields.Float(string="Voc (V)")
    imp = fields.Float(string="Imp (A)")
    vmp = fields.Float(string="Vmp (V)")
    fuse_rating = fields.Char(string="Fuse Rating & Sytem Voltage")
    remarks = fields.Char(string='Remarks')
    year_of_mfg = fields.Selection(
        [('2015', '2015'), ('2016', '2016'), ('2017', '2017'),
         ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'),
         ('2024', '2024'), ('2025', '2025'), ('2026', '2026'),
         ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'),
         ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'),
         ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040'), ('2041', '2041'), ('2042', '2042'),
         ('2043', '2043'),
         ('2044', '2044'), ('2045', '2045'), ],
        default='2015', string="Year of Mfg", tracking=True)
    state = fields.Selection(
        [('accepted', 'Accepted'), ('rejected', 'Rejected')],
        string="Status")

    sample_request_id = fields.Many2one('sample.form', string="Sample Request", invisible=True)









