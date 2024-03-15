# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
##############################################################################

{
    'name': 'Bz Payroll',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Bz Payroll',
    'description':
        """
       Bz Payroll

    """,
    'summary': 'Bz Payroll',
    'depends': ['hr_contract', 'om_hr_payroll', 'hr_contract_types', 'report_xlsx', 'om_hr_payroll_account'],
    'data': [
        'security/ir.models.access.csv',
        'security/security.xml',
        'data/contract_data.xml',
        'data/hr_contract_type.xml',
        'data/section_data.xml',
        'data/salary_rule.xml',
        'data/mail_template.xml',
        'data/hr_contract_type.xml',
        'data/ir_sequence.xml',
        'views/res_config.xml',
        'views/investment_declaration_sections.xml',
        'views/investment.xml',
        'views/contract.xml',
        'views/hr_views.xml',
        'views/payslip_views.xml',
        'views/report_payslip.xml',
        'views/payroll_report.xml',
        'views/batch_account_details.xml',
        'views/employee_account_details_view.xml',
        'views/pay_structures_view.xml',
        'views/ir_cron.xml',
        'wizard/multy_payroll_wizard.xml',
        'wizard/multi_payroll_confirm_view.xml',
        'report/report.xml',
        'report/investment_pdf_report.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
