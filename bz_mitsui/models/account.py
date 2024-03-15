from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _notification_advance_payment(self):
        partial_paid = self.env['account.move'].search([('payment_state', '=', 'partial'), ('move_type', 'in', ['out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt'])])
        if partial_paid:
            for rec in partial_paid:
                # template = self.env.ref('bz_sample_request.mail_template_goahead', False)
                mtp = self.env['mail.template']
                ir_model_data = self.env['ir.model.data']
                template_id = ir_model_data.get_object_reference('bz_mitsui',
                                                                 'advance_payment_notification')
                mail_tem = mtp.browse(template_id[1])
                body = """Dear All,<br/><br/>
                        update the log for the invoice %s <br/><br/>
                        Best Regards;
                        Administrator
                        """% (rec.name)
                mail_tem.write({'email_to': rec.invoice_user_id.login,
                                # 'email_cc': rec.invoice_user_id.login,
                                'body_html': body})
                # sale = sale_order = sale_order_map.get(move_line.id)
                mail_tem.send_mail(self.id, True)

   