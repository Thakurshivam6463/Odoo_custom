# -*- coding: utf-8 -*-

{
    'name': 'Project Templates',
    'version': '14.0.1.0.0',
    'category': "Project",
    'summary': """This app allows your project team to create project template and task template""",
    'depends': ['base', 'project', 'sale'],
    'data': [
        'views/project_task.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
