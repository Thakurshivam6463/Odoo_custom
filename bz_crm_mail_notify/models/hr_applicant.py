from odoo import models, api, _


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    @api.model
    def create(self, vals):
        applicant = super(HrApplicant, self).create(vals)
        template = self.env.ref('bz_crm_mail_notify.mail_template_hr_applicant',
                                raise_if_not_found=False)
        if applicant.email_from:
            if template:
                email_values = {'email_from': 'technologiesbonzapro@gmail.com' or '',
                                'email_to': applicant.email_from}
                template.send_mail(applicant.id, email_values=email_values, force_send=True)
        return applicant

