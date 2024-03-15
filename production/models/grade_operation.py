# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class GradeGrade(models.Model):
    _name = 'grade.grade'
    _rec_name = 'name'

    name = fields.Char("Grade Name")
    is_sub_grade = fields.Boolean("Is Sub Grade?")

    
class GradeOperation(models.Model):
    _name = 'grade.operation'
    _rec_name = 'name'

    name = fields.Char("Grade Name", default=lambda self: self.env['ir.sequence'].next_by_code('grade.operation'))
    batch_id = fields.Many2one('fish.batch', 'Batch')
    receiving_id = fields.Many2one('materials.reciving.deck', 'Materials Receiving')
    status = fields.Selection([('draft', 'Draft'), ('verifying', 'Verifying'), ('complete', 'Complete')], default='draft', string="Stage")
    grade_operation_line_ids = fields.One2many('grade.operation.lines', 'grade_operation_id', 'Grade Operation')


class GradeOperationLines(models.Model):
    _name = 'grade.operation.lines'
    _rec_name = 'grade_id'

    grade_id = fields.Many2one("grade.grade", string="Grade Name")
    weight = fields.Float(string="Weight")
    count = fields.Integer(string="Count")
    is_sub_grade_id = fields.Many2one("grade.grade", string="Is Sub Grade", domain=[('is_sub_grade', '=', True)])
    grade_operation_id = fields.Many2one("grade.operation", string="Grade Operation")