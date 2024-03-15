from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BatchAccountDetails(models.Model):
    _name = "batch.account.details"
    _description = 'Batch Account Details'
    _rec_name = 'debit_branch_id'

    debit_customer_id = fields.Char(string='Debit Customer ID')
    debit_branch_id = fields.Char(string='Debit Branch ID')
    debit_account_no = fields.Char(string='Debit account Number')
    serial_no = fields.Char(string='Serial No')

    @api.model
    def create(self, vals):
        record_available = self.search([])
        if record_available:
            raise ValidationError(_(
                'There is already a record created.'))
        res = super(BatchAccountDetails, self).create(vals)
        return res


