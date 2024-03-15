from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Sale(models.Model):
    _inherit = ['sale.order']

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sales_pic', 'Sales PIC'),
        ('sales_manager', 'Sales Manager'),
        ('general_manager', 'General manager'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def action_sales_pic(self):
        self.state = 'sales_pic'

    def approve_sales_pic(self):
        if self.env.user.has_group('bz_crm_trf.group_sales_pic_user'):
            self.state = 'sales_manager'
        else:
            raise ValidationError(
                _(
                    "Only Sales PIC can approved this order."
                )
            )

    def action_sales_manager(self):
        if self.env.user.has_group('bz_crm_trf.group_sales_manager'):
            self.state = 'general_manager'
        else:
            raise ValidationError(
                _(
                    "Only Sales Manger can approved this order."
                )
            )

    def action_general_manager(self):
        if self.env.user.has_group('bz_crm_trf.group_general_manager'):
            self.state = 'sale'
        else:
            raise ValidationError(
                _(
                    "Only General Manager can approved this order."
                )
            )






