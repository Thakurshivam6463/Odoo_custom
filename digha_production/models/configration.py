# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError

# master data for grade count
class GradeCount(models.Model):
    _name = 'grade.count'

    grade_count = fields.Char(string="Grade Count")



# master data for valueaddproduct

class ValueAddProduct(models.Model):
    _name = 'valueadd.product'

    value_add_product = fields.Char(string="Value Add Product")


# master data for valueaddproduct

class Time(models.Model):
    _name = 'start.time'

    froms = fields.Float(string="From")
    to = fields.Float(string="To")


# master data for valueaddproduct

class Freezer(models.Model):
    _name = 'freezer'

    freezer = fields.Char(string="Freezer")



