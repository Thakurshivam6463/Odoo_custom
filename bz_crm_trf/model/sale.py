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
    scope_matrix_id = fields.Many2one('scope.matrix', string='Scope Matrix')

    def action_sales_pic(self):
        #self.state = 'sales_pic'
         if self.env.user.has_group('bz_crm_trf.group_sales_pic_user'):
             self.state = 'sales_pic'
         else:
             raise ValidationError(
                 _(
                     "Only Sales PIC can approved this order."
                 )
             )


    def approve_sales_pic(self):
        if self.env.user.has_group('bz_crm_trf.group_sales_manager'):
            self.state = 'sales_manager'
        else:
            raise ValidationError(
                _(
                    "Only Sales PIC can approved this order."
                )
            )
    def action_sales_manager(self):
        if self.env.user.has_group('bz_crm_trf.group_general_manager'):
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

    def action_cancel(self):
        self.state = 'cancel'

class SaleStandard(models.Model):
    _inherit = ['sale.order.line']
    
    standard_id = fields.Many2one('standards', string="Standard")




