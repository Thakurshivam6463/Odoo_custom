from odoo import models, fields, api, _

class InvestmentDeclarationSections(models.Model):
    _name = "investment.declaration.sections"
    _description = 'Investment Declaration Sections'
    _rec_name = 'section'

    section = fields.Char(string='Section', required=True)
    expense_line = fields.One2many('investment.declaration.sections.line', 'section_id', 'Expense')
    max_limit = fields.Char(string='Max Limit')
    code = fields.Char('Code')

class InvestmentDeclarationSectionsLine(models.Model):
    _name = "investment.declaration.sections.line"
    _description = 'Investment Declaration Sections Line'
    _rec_name = 'expense'

    section_id = fields.Many2one('investment.declaration.sections', string='Section')
    expense = fields.Char(string='Head')
    description = fields.Char(string='Description')



