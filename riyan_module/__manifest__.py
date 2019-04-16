# -*- coding: utf-8 -*-
{
    'name': "RFPs_module",

    'summary': """
        Complete RFPs Managment""",

    'description': """
         All About Tender Managment
    """,

    'author': "Riyan.p",
    'website': "http://www.greenit.com.np",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'library',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','mail'],
    
    # always loaded
    'data': [
        #security
        'security/user_group.xml',
        'security/ir.model.access.csv',
        #data
        'data/ir_config_parameter.xml',
        'data/res_groups.xml',
        'data/res_company_data.xml',
        #report
        'report/report_template.xml',
        'report/bank_guarentee_report.xml',
        'report/bank_indemnity_form.xml',
        #view   
        'views/tendermanagment_view.xml',
        'views/category_view.xml',
        'views/companylist_view.xml',
        'views/banklist_view.xml',
        'views/bank_application_form_view.xml',
        'views/bank_application_email.xml',
        'views/vendor_view.xml',
        'views/tenderemail_templet_view.xml',
        'views/email_templet_view.xml',
        'views/notification_email_template.xml',
        'views/res_config_setting_view.xml',
        'views/riyan_module_customize_view.xml',
        'views/ir_model_view.xml',
        'views/webclient_template.xml',
        'views/res_company_view.xml',
        #'views/gits_report_saleorder.xml',
    ],
    'qweb': [
        'static/src/xml/base.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    "auto_install": False,
    "installable": True,
}