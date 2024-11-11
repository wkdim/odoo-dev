# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Recruitment',
    'version': '1.1',
    'category': 'Human Resources/Recruitment',
    'sequence': 90,
    'description': 'My work',
    'summary': 'For Recruitment Questions',
    'depends': [
        'hr',       
        'hr_recruitment'],
    'data': [
                'security/ir.model.access.csv',
                'views/question.xml',
                'views/ratings.xml',
                'views/stages.xml',



    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        
    },
    'license': 'LGPL-3',
}
