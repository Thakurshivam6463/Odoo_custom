# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api


class testing_checklist(models.Model):
    _name = 'testing.checklist'
    _description = 'Testing Checklist'
    
    name = fields.Char('Name', required="1")
    code = fields.Char('Code')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
