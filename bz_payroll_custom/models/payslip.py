from odoo import models, fields, api, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    company_id = fields.Many2one('res.company', store=True, default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    basic = fields.Monetary(string="Basic")
    hra = fields.Monetary(string="HRA")
    conveyance_allowance = fields.Monetary(string="Conveyance Allowance")
    food_allowance = fields.Monetary(string="Food Allowance")
    medical_allowance = fields.Monetary(string="Medical Allowance")
    special_allowance = fields.Monetary(string="Special Allowance")
    rent_line = fields.One2many('payslip.rent.line', 'payslip_id', 'House Rent Declaration')
    investment_line = fields.One2many('payslip.investment.line', 'payslip_id', 'Investment Declaration')
    hra_exemption = fields.Monetary(string="HRA Exemption")

    def net_salary(self, contract, categories):
        net_income = 0.0
        net_salary = 0.0
        gross_salary = 0.0
        declared_amount = 0.0
        monthly_investment = 0.0
        if contract:
            gross_salary = contract.wage + contract.hra_exemptions + contract.conveyance_allowance + contract.meal_allowance + contract.medical_allowance + contract.other_allowance
            gross_salary = gross_salary - (50000 / 12)
        if contract.employee_id:
            investment = self.env['investment.declaration'].search([('employee_id', '=', contract.employee_id.id)], limit=1)
            if investment:
                for line in investment.investment_line:
                    declared_amount += line.declared_amount
            if declared_amount:
                monthly_investment = declared_amount/12
        net_income = gross_salary - monthly_investment
        net_salary = net_income - (contract.pt + contract.tds) - categories.DED
        if contract.pf:
            pf_amount = (net_salary * int(contract.pf))/100
            net_salary -= pf_amount
        return round(net_salary, 2)

    def compute_sheet(self):
        res = super(HrPayslip, self).compute_sheet()
        contract_ids = self.contract_id.ids or \
                       self.get_contract(self.employee_id, self.date_from, self.date_to)
        for contract in contract_ids:
            contract_obj = self.env['hr.contract'].browse(contract)
            if contract_obj:
                self.write({'basic': contract_obj.wage,
                            'hra': contract_obj.hra,
                            'conveyance_allowance': contract_obj.conveyance_allowance,
                            'food_allowance': contract_obj.meal_allowance,
                            'medical_allowance': contract_obj.medical_allowance,
                            'special_allowance': contract_obj.other_allowance,
                            'hra_exemption': contract_obj.hra_exemptions
                            })
            investment = self.env['investment.declaration'].search([('employee_id', '=', self.employee_id.id)],
                                                                   limit=1)
            if investment:
                for investment_line in investment.investment_line:
                    self.investment_line = [
                        (0, 0, {
                            'section': investment_line.section.id,
                            'description': investment_line.description,
                            'max_limit': investment_line.max_limit,
                            'declared_amount': investment_line.declared_amount,
                            'expense': investment_line.expense.id
                        }),
                                            ]
                for hra_line in investment.house_rent_line:
                    self.rent_line = [
                        (0, 0, {
                            'landlord_name': hra_line.landlord_name,
                            'street': hra_line.street,
                            'pan': hra_line.pan,
                            'accommodation_address': hra_line.accommodation_address,
                            'city': hra_line.city,
                            'rent_Payable': hra_line.rent_Payable,
                            'rent_effective_from': hra_line.rent_effective_from,
                            'rent_effective_to': hra_line.rent_effective_to
                        }),
                    ]
        return res

    def unpaid_leaves(self, contract, payslip, worked_days):
        #Net salary calculation
        net_income = 0.0
        net_salary = 0.0
        gross_salary = 0.0
        declared_amount = 0.0
        monthly_investment = 0.0
        lop_amount = 0.0
        if contract:
            gross_salary = contract.wage + contract.hra_exemptions + contract.conveyance_allowance + contract.meal_allowance + contract.medical_allowance + contract.other_allowance
            gross_salary = gross_salary - (50000 / 12)
        if contract.employee_id:
            investment = self.env['investment.declaration'].search([('employee_id', '=', contract.employee_id.id)],
                                                                   limit=1)
            if investment:
                for line in investment.investment_line:
                    declared_amount += line.declared_amount
            if declared_amount:
                monthly_investment = declared_amount / 12
        net_income = gross_salary - monthly_investment
        net_salary = net_income - (contract.pt + contract.tds)
        #Leave calculation
        st_date = payslip.date_from
        en_date = payslip.date_to
        month_day_count = abs((en_date - st_date).days)
        month_day_count += 1
        per_day_salary = net_salary / month_day_count
        if worked_days.Unpaid != 0.0:
            unpaid_leave = worked_days.Unpaid.number_of_days
            lop_amount = per_day_salary * unpaid_leave
        if lop_amount:
            return round(lop_amount, 2)
        return 0.0

class PayslipRentLine(models.Model):
    _name = "payslip.rent.line"
    _description = 'House Rent Line'

    payslip_id = fields.Many2one('hr.payslip', string='Payslip Id')
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

class PayslipInvestmentLine(models.Model):
    _name = "payslip.investment.line"
    _description = 'Investment Line'

    payslip_id = fields.Many2one('hr.payslip', string='Payslip Id')
    section = fields.Many2one('investment.declaration.sections', string='Section')
    description = fields.Char(string='Description')
    company_id = fields.Many2one('res.company', store=True, default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    max_limit = fields.Monetary(string='Max Limit')
    declared_amount = fields.Monetary(string='Declared Amount')
    expense = fields.Many2one('investment.declaration.sections.line', string='Head')

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    @api.onchange('date_start', 'date_end')
    def onchange_period(self):
        if self.date_start and self.date_end:
            payslips = self.env['hr.payslip'].search([('date_from', '<=', self.date_start), ('date_to', '<=', self.date_end)])
            if payslips:
                self.slip_ids = [(6, 0, payslips.ids)]

