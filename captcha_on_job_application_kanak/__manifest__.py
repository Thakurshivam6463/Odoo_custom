# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Captcha On Job Application',
    'version': '1.0',
    'summary': 'This module is used to applied Recaptcha on login in job application form on website.| Captcha | ReCaptcha | ReCaptcha Configuration | Recruitment | HR Recruitment | Jobs | Human Resources | HR | Employees | Job Application',
    'description': """Google captcha on job application form""",
    'category': 'Human Resources/Recruitment',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'images': ['static/description/banner.jpg'],
    'depends': ['website_hr_recruitment'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'sequence': 1,
    'installable': True,
    'application': False,
    'auto_install': False,
}
