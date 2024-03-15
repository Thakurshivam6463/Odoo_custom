# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class OrderReportWizard(models.TransientModel):
    _name = "order.report.wizard"
    _description = "Print Order Wizard"

    product_id = fields.Many2one('electronic.product', string="Product")
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_print_excel_report(self):

        domain = []
        product_id = self.product_id
        if product_id:
            domain += [('product_id', '=', product_id.id)]
        date_from = self.date_from
        if date_from:
            domain += [('date_order', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('date_order', '<=', date_to)]

        orders = self.env['electronic.order'].search_read(domain)
        data = {
            'orders': orders,
            'form_data': self.read()[0],
        }
        return self.env.ref('electronic_item.report_product_order_xlsx').report_action(self, data=data)

    def action_print_report(self):
        domain = []
        product_id = self.product_id
        if product_id:
            domain += [('product_id', '=', product_id.id)]
        date_from = self.date_from
        if date_from:
            domain += [('date_order', '>=', date_from)]
        date_to = self.date_to
        if date_to:
            domain += [('date_order', '<=', date_to)]

        #orders = self.env['electronic.order'].search_read(domain)
        orders = self.env['electronic.order'].search(domain)
        order_list = []
        for order in orders:
            vals = {
                'name': order.name,
                'note': order.note,
                'price': order.price,
            }
            order_list.append(vals)
        data = {
            'form_data': self.read()[0],
            'orders': order_list
            }
        return self.env.ref('electronic_item.action_report_order_custom').report_action(self, data=data)
        # return self.env('ga_electronic.action_report_order').report_action(self, data=data)
