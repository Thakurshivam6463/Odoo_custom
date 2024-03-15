from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime
from datetime import date, datetime, timedelta, time


class InvestmentDeclaration(models.Model):
    _name = "investment.declaration"
    _description = 'Investment Declaration'
    _rec_name = 'employee_id'

    name = fields.Char('Name')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    employee_identification = fields.Char(string='Employee ID')
    joining_date = fields.Date(string='Date of Joining')
    employee_pan = fields.Char(string='PAN')
    mobile = fields.Char('Mobile')
    investment_line = fields.One2many('investment.declaration.line', 'investment_id', 'Investment')
    house_rent_line = fields.One2many('house.rent.line', 'investment_dec_id', 'Investment')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    modification_end_date = fields.Date(string='Modification End Date', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('bz_payroll_custom.modification_end_date') or False, readonly=True)

    def get_financial_year(self):
        date_start = date(date.today().year, 1, 1)
        date_end = date(date.today().year, 12, 31)
        return str(date_start) + ' - ' + str(date_end)

    @api.model_create_multi
    def create(self, vals):
        code = []
        rec_ids = []
        declared_amount = 0.0
        max_limit = 0.0
        data = vals[0]
        if data.get('investment_line'):
            for line in data.get('investment_line'):
                if line[2]:
                    data = line[2]
                    if data.get('code') != 'under_sec_80c':
                        code.append(data.get('code'))
                        rec_ids.append(data.get('expense'))
                    if data.get('code') == 'under_sec_80c':
                        max_limit = data.get('max_limit')
                        declared_amount += data.get('declared_amount')
            if len(code) == len(set(code)) or len(rec_ids) == len(set(rec_ids)):
                pass
            else:
                raise ValidationError(_(
                    'You can not add the same investment.'))
            if declared_amount > max_limit:
                raise ValidationError(_(
                    'You can not exceed the Max Limit.'))
        res = super(InvestmentDeclaration, self).create(vals)
        # duplicate = self.search([('employee_id', '=', res.employee_id.id)])
        # if duplicate:
        #     raise ValidationError(_(
        #         'Investment Declaration already created for this employee.'))
        # modification_date = self.env['ir.config_parameter'].sudo().get_param('bz_payroll_custom.modification_end_date')
        # date_obj = datetime.strptime(modification_date, '%Y-%m-%d')
        # kk = datetime.today()
        # if modification_date < datetime.today():
        #     raise ValidationError(_(
        #         'You exceed the modification date.')) #Todo
        return res

    def write(self, vals):
        declared_amounts = 0.0
        max_limit = 0.0
        code = []
        rec_ids = []
        if self.modification_end_date:
            if self.modification_end_date < date.today():
                raise ValidationError(_(
                    'You exceed the modification date.'))
        if vals.get('investment_line'):
            if self.investment_line:
                for record in self.investment_line:
                    if record.code != 'under_sec_80c':
                        code.append(record.code)
                        rec_ids.append(record.expense.id)
                    if record.code == 'under_sec_80c':
                        declared_amounts += record.declared_amount
                        max_limit = record.max_limit
            for line in vals.get('investment_line'):
                if line[2]:
                    data = line[2]
                    if data.get('code') != 'under_sec_80c':
                        code.append(data.get('code'))
                        rec_ids.append(data.get('expense'))
                    if data.get('code') == 'under_sec_80c':
                        max_limit = data.get('max_limit')
                        declared_amounts += data.get('declared_amount')
            if len(code) == len(set(code)) or len(rec_ids) == len(set(rec_ids)):
                pass
            else:
                raise ValidationError(_(
                    'You can not add the same investment.'))
            if declared_amounts > max_limit:
                raise ValidationError(_(
                    'You can not exceed the Max Limit.'))
        if vals.get('house_rent_line'):
            from_date = False
            for req_line in vals.get('house_rent_line'):
                if req_line[2]:
                    data1 = req_line[2]
                    if req_line[0] == 0:
                        from_date = data1.get('rent_effective_from')
            for house_rent_line in self.house_rent_line:
                if from_date:
                    date_type_format = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
                    if date_type_format < house_rent_line.rent_effective_to and date_type_format > house_rent_line.rent_effective_from:
                        raise ValidationError(
                            _('Time period of house rent is overlapping.'))
        res = super(InvestmentDeclaration, self).write(vals)
        return res

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.employee_identification = self.employee_id.identification_id
            self.joining_date = self.employee_id.joining_date
            self.employee_pan = self.employee_id.pan
            self.mobile = self.employee_id.mobile

    def action_calculate_tds(self):
        pass

    @api.model
    def get_validation_date(self):
        icp_sudo = self.env['ir.config_parameter'].sudo()
        modification_end_date = icp_sudo.get_param('bz_payroll_custom.modification_end_date')
        date_type_format = datetime.strptime(modification_end_date, '%Y-%m-%d').date()
        notification_date = date_type_format - timedelta(days=7)
        if datetime.today().date() == notification_date:
            employee_ids = self.env['hr.employee'].search([('active', '=', True)])
            template = self.env.ref('bz_payroll_custom.mail_template_investment_declaration_date',
                                    raise_if_not_found=False)
            if employee_ids:
                for employee in employee_ids:
                    investment_declaration = self.env['investment.declaration'].search([('employee_id', '=', employee.id)], limit=1)
                    if investment_declaration:
                        if template:
                            email_values = {'email_from': self.env.user.email or '',
                                            'email_to': investment_declaration.employee_id.work_email}
                            template.send_mail(investment_declaration.id, email_values=email_values, force_send=True)


class InvestmentDeclarationLine(models.Model):
    _name = "investment.declaration.line"

    investment_id = fields.Many2one('investment.declaration', string='Investment Id')
    section = fields.Many2one('investment.declaration.sections', string='Section')
    description = fields.Char(string='Description')
    max_limit = fields.Float(string='Max Limit')
    declared_amount = fields.Float(string='Declared Amount')
    document = fields.Binary('Document')
    expense = fields.Many2one('investment.declaration.sections.line', string='Head')
    code = fields.Char('Code')

    @api.onchange('section')
    def _onchange_section(self):
        if self.section:
            section_line = self.env['investment.declaration.sections.line'].search([('section_id', '=', self.section.id)])
            return {'domain': {'expense': [('id', '=', section_line.ids)]}}

    @api.onchange('expense')
    def _onchange_expense(self):
        max_limit = 0.0
        if self.expense:
            self.description = self.expense.description
            if not self.expense.section_id.code == 'under_sec_80e':
                self.max_limit = self.expense.section_id.max_limit
            self.code = self.expense.section_id.code

    @api.onchange('declared_amount')
    def _onchange_declared_amount(self):
        if self.declared_amount:
            if self.max_limit:
                if self.max_limit < self.declared_amount:
                    raise ValidationError(_(
                        'You can not exceed the Max Limit.'))


class HouseRentLine(models.Model):
    _name = "house.rent.line"
    _description = 'House Rent Line'

    investment_dec_id = fields.Many2one('investment.declaration', string='Investment Id')
    landlord_name = fields.Char(string='Landlord Name')
    street = fields.Char('Street')
    pan = fields.Char('PAN')
    accommodation_address = fields.Char(string='Accommodation Address')
    city = fields.Char(string='City')
    company_id = fields.Many2one('res.company', store=True,default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    rent_Payable = fields.Monetary(string="Rent Payable")
    rent_effective_from = fields.Date(string='Rent Effective From')
    rent_effective_to = fields.Date(string='Rent Effective To')
    document = fields.Binary('Document')
    type = fields.Selection([('10_of_salary', '10% of salary'), ('50_of_basic_salary', '50% of basic salary')], 'Type',
                              default='10_of_salary')
    calculated_price = fields.Float(string='Calculated Price', default=0.0)

    @api.onchange('type', 'rent_Payable')
    def _onchange_type(self):
        if self.rent_Payable and self.type:
            contract = self.env['hr.contract'].search([('employee_id', '=', self.investment_dec_id.employee_id.id), ('state', '=', 'open')], limit=1)
            if contract:
                if self.type == '10_of_salary':
                    basic = contract.wage
                    amount = (basic * 10)/100
                    exemption = self.rent_Payable - amount
                    hra_exemption = contract.hra - exemption
                    self.calculated_price = hra_exemption
                    contract.hra_exemptions = hra_exemption
                else:
                    self.calculated_price = contract.hra
                    contract.hra_exemptions = contract.hra

