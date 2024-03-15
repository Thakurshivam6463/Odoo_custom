from odoo import models, api, _


class Lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create(self, vals):
        lead = super(Lead, self).create(vals)
        template = self.env.ref('bz_crm_mail_notify.mail_template_lead_notify',
                                raise_if_not_found=False)
        if lead.email_from:
            if template:
                email_values = {'email_from': 'technologiesbonzapro@gmail.com' or '',
                                'email_to': lead.email_from}
                template.send_mail(lead.id, email_values=email_values, force_send=True)
        return lead

