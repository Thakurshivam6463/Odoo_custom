import math
import re
from odoo import api, models, fields, _

class ProjectBarcode(models.Model):
    _inherit = 'project.project'

    barcode = fields.Char('Barcode')
    po_barcode_setting = fields.Boolean('PO Barcode Setting')
    sample_id = fields.Many2one('sample.form', string='Sample')
    
    def action_sample_view(self):
        if self.sale_order_id:
            sale_ids = self.env['sample.form'].search([('sale_order_id', '=', self.sale_order_id.id)]).ids
            return {
                'type': "ir.actions.act_window",
                'name': 'Sample',
                "res_model": "sample.form",
                "domain": [("id", "in", sale_ids)],
                "view_mode": "tree,form",
                'target': 'current',
            }

    def action_trf_view(self):
        if self.sale_order_id.scope_matrix_id.trf_id:
            return {
                'type': "ir.actions.act_window",
                'name': 'TRF',
                "res_model": "trf",
                "domain": [("id", "=", self.sale_order_id.scope_matrix_id.trf_id.id)],
                "view_mode": "tree,form",
                'target': 'current',
            }

    def action_reject(self):
        if self.sale_order_id:
            mtp = self.env['mail.template']
            ir_model_data = self.env['ir.model.data']
            template_id = ir_model_data.get_object_reference('bz_sample_request',
                                                             'mail_template_project_reject')
            mail_tem = mtp.browse(template_id[1])
            mail_tem.write({'email_to': self.sale_order_id.user_id.login})
            mail_tem.send_mail(self.id, True)
            print('Mail Sent')
            return True
            # message = _("Provided document need recheck.")
            # return self.sale_order_id.message_post(body=message)

    @api.model
    def create(self, vals):
        # settings_barcode = self.env['ir.config_parameter'].sudo().get_param('bz_barcode_number_print.is_purchase_order_barcode')
        # vals.update({
        #     'po_barcode_setting': settings_barcode
        # })
        res = super(ProjectBarcode, self).create(vals)
        barcode_id = res.name
        barcode_search = False
        while not barcode_search:
            ean = generate_ean(str(barcode_id))
            if self.env['project.project'].search([('barcode', '=', ean)]):
                barcode_search = False
                barcode_id += str(1)
            else:
                barcode_search = True
        res.barcode = ean
        return res

    def get_sample_data(self, sale_order_id):
        sample_ids = self.env['sample.form'].search([('sale_order_id', '=', sale_order_id)])
        return sample_ids


def ean_checksum(eancode):
    """returns the checksum of an ean string of length 13, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 13:
        return -1
    oddsum = 0
    evensum = 0
    eanvalue = eancode
    reversevalue = eanvalue[::-1]
    finalean = reversevalue[1:]

    for i in range(len(finalean)):
        if i % 2 == 0:
            oddsum += int(finalean[i])
        else:
            evensum += int(finalean[i])
    total = (oddsum * 3) + evensum

    check = int(10 - math.ceil(total % 10.0)) % 10
    return check

def generate_ean(ean):
    """Creates and returns a valid ean13 from an invalid one"""
    if not ean:
        return "0000000000000"
    ean = re.sub("[A-Za-z]", "0", ean)
    ean = re.sub("[^0-9]", "", ean)
    ean = ean[:13]
    if len(ean) < 13:
        ean = ean + '0' * (13 - len(ean))
    print("barcode : ", ean[:-1] + str(ean_checksum(ean)))
    return ean[:-1] + str(ean_checksum(ean))
