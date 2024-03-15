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



class sale_order(models.Model):
    _inherit = 'sale.order'
    
    testing_lines = fields.One2many('project.testing','order_id', string='Testing Lines')
    project_id = fields.Many2one('project.project', copy=False)
    
    def action_confirm(self):
        line_id = False
        res = super(sale_order, self).action_confirm()
        for line in self.order_line:
            line_id = line.id
        if line_id:
            project_task = self.env['project.task'].search([('sale_line_id', '=', line_id)])
            project_obj = project_task.project_id
            if project_obj:
                for line_data in self.order_line:
                    task = self.env['project.task'].search([('project_id', '=', project_obj.id),
                                                            ('name', '=', line_data.product_id.name)])
                    if task:
                        task.active = False
                if self.project_template_id:
                    for item in self.project_template_id.task_ids:
                        project_obj.create_task(item, False)
                        # task = self.env['project.task'].create({
                        #     'name': project_task.name,
                        #     'project_id': project_obj.id,
                        #     'recurring_task': True,
                        #     'sale_line_id': self.id,
                        #     'partner_id': self.partner_id.id,
                            # 'repeat_interval': 1,
                            # 'repeat_unit': 'week',
                            # 'repeat_type': 'after',
                            # 'repeat_number': 2,
                            # 'mon': True,
                        # })
                        # if task:
                        #     project_obj.task_ids = task.ids
                        #     print('gggg')

        if self.testing_lines:
            ana_account_id = self.env['account.analytic.account'].create({
                'name':self.name,
                'partner_id':self.partner_id and self.partner_id.id or False,
                'company_id':self.company_id and self.company_id.id or False,
                'currency_id':self.currency_id and self.currency_id.id or self.company_id.currency_id.id or False,
            })
            stage_ids = self.company_id.project_stage_ids.ids or []
            project_id = self.env['project.project'].create({
                'name':self.name,
                'partner_id':self.partner_id and self.partner_id.id or False,
                'privacy_visibility':'employees',
                'analytic_account_id':ana_account_id and ana_account_id.id or False,
                'type_ids':[(6,0, stage_ids)],
                'sale_id':self.id,
            })
            if project_id:
                self.project_id = project_id.id
                # if self.project_template_id:
                #     for project_task in self.project_template_id.task_ids:
                #
                #         task = self.env['project.task'].create({
                #             'name': project_task.name,
                #             'project_id': self.project_id.id,
                #             'recurring_task': True,
                #             'sale_line_id': self.id,
                #             'partner_id': self.partner_id.id,
                            # 'repeat_interval': 1,
                            # 'repeat_unit': 'week',
                            # 'repeat_type': 'after',
                            # 'repeat_number': 2,
                            # 'mon': True,
                        # })
                
        return res



class project_testing(models.Model):
    _name = 'project.testing'
    _description = 'Project Testing'
    
    sequence = fields.Integer(string='Sequence', default=10)
    testing_id = fields.Many2one('dev.testing', required="1")
    checklist_ids = fields.Many2many('testing.checklist', string='Checklist')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    location_id = fields.Many2one('dev.testing.location', string='Location')
    
    @api.onchange('testing_id')
    def onchange_testing(self):
        if self.testing_id:
            self.checklist_ids = self.testing_id.checklist_ids
        else:
            self.checklist_ids = False



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
