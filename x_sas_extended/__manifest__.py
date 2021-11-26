# -*- coding: utf-8 -*-
{
    'name': "x_sas_extended",

    'summary': "Technical tests module",

    'description': """
        Technical 
        Tests 
        Module
    """,

    'author': "Reyes Hernando Santana Perez",
    'website': "inghernandosan@outlook.com",

    'category': 'Uncategorized',
    'version': '14.0.1',

    'depends': [
        'base',
        'product'
    ],

    # always loaded
    'data': [
        'security/res_group_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/service_mail_template.xml',
        'views/service_guide_view.xml',
        'views/service_graph_view.xml',
        'views/service_category_view.xml',
        'report/report_service_guide.xml',
    ],

    "installable": True,
}
