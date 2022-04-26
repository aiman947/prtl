# -*- coding: utf-8 -*-
{
    'name': "OdooCMS Employee Portal",
    'summary': """Employee Web Portal""",
    'description': """Web Portal for Employee""",
    'author': "Infinite Scaleup &amp; Farooq Arif",
    'company': 'Student Portal',
    'website': "https://www.employee.com",
    'category': 'Employee Portal',
    'version': '1.0',
    'sequence': '1',
    'application': 'true',
    'depends': ['base','website', 'stock','website_sale','hr','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_portal_login.xml',
        'views/leaves_portal_templates.xml',
        # 'views/test_report.xml',
        'views/customer_partner_form.xml',
        'wizards/computation_wizard.xml',

        'reports/reports.xml',
        'reports/notice_report.xml',
    ],
}
