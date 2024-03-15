from odoo import models, fields, api, _

class CustomPurchaseDashboard(models.Model):
    _name = "custom.purchase.dashboard"

    color = fields.Integer(string='Color Index')
    name = fields.Char(string="Name")

    def dashboard_rfq_action_id(self):
        print('fffffff')

    def dashboard_purchase_action_id(self):
        print('fffffff')