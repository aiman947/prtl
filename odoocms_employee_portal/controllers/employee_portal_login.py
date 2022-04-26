import json
import pdb

import sudo as sudo

from odoo import http, SUPERUSER_ID
from odoo.http import request
from datetime import date
import json
from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slugify
from odoo.addons.web.controllers.main import ReportController

import re
from odoo import fields, models, _, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.tools.safe_eval import safe_eval
import pdb
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from odoo.http import content_disposition, Controller, request, route
import random


class CataloguePrint(http.Controller):

    @http.route(['/report/pdf/catalogue_download'], type='http', auth='public')
    def download_catalogue(self, employee_id):
        print(1112222333333333, employee_id)

        pdf, _ = request.env.ref('odoocms_employee_portal.employee_action_report').sudo(). \
            render_qweb_pdf([int(employee_id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition', 'catalogue' + '.pdf;')]
        return request.make_response(pdf, headers=pdfhttpheaders)


class EmployeeLoginDashboard(http.Controller):
    @http.route(['/employee/dashboard'], type='http', auth="user", website=True)
    def employee_home(self, **kw):
        payslip_id = request.env['hr.employee'].sudo().search([])
        return request.render("odoocms_employee_portal.employee_reportsss", {
            'payslip_id': payslip_id,
        })

        # @http.route('/employee/dashboard2/<model("hr.employee"):so>/', type='http', auth="user", website=True)

        @http.route(['/employee/dashboard2'], type='http', auth="public", website=True)
        def employee_page(self, so, **kw):
            return request.render("odoocms_employee_portal.employee_portal_dashboard_page", {
                'emp': so
            })

        # @http.route(['/employee/report'], type='http', auth="user", website=True)
        # def employee_report(self, **kw):
        #     return request.render("odoocms_employee_portal.employee_payslips_template")

        ###############################################################################


class EmployeeReport(http.Controller):

    @http.route(['/employee/report'], type='http', auth="user", website=True)
    def employee_report(self, **kw):
        current_user = http.request.env.user
        print(current_user, "Current user  ----------------------")

        payslip_id = request.env['hr.employee'].sudo().search([])
        pays_id = request.env['hr.employee'].sudo().search([('current_user', '=', 'employee_id')])
        payslipppss_id = request.env['hr.payslip'].sudo().search([('current_user', '=', 'employee_id')])

        rule_id = request.env['hr.salary.rule'].sudo().search([])
        # docs = request.env['hr.employee'].browse(request.env.context.get('active_id'))
        # docs = pays_id
        datas = {
            'rule_id': rule_id,
            'pays_id': pays_id,
            'payslipppss_id': payslipppss_id,
            # 'docs': docs
        }
        return request.render("odoocms_employee_portal.employee_report_template", datas)


class EmployeeDetails(http.Controller):

    @http.route(['/employee/details'], type='http', auth="user", website=True)
    def employee_report(self, **kw):
        # test = self.user_id
        # print(test)

        current_user = http.request.env.user
        # pay_emp_id = request.env['hr.employee'].sudo().search([('employee_id', '=', current_user.name)])
        payslip_id = request.env['hr.payslip'].sudo().search([('employee_id', '=', current_user.name)])

        return request.render("odoocms_employee_portal.employee_payslips_template",
                              {'payslip_id': payslip_id})


class LeavesEmployee(http.Controller):

    @http.route(['/leaves/details'], type='http', auth="user", website=True)
    def leaves_details(self, **kw):
        current_user = http.request.env.user
        leaves_id = request.env['hr.payslip'].sudo().search([('employee_id', '=', current_user.name)])
        return request.render("odoocms_employee_portal.employee_leaves_template",
                              {'leaves_id': leaves_id, }
                              )


class LeavesformSubmit(http.Controller):
    # mention class name
    @http.route(['/leaves/form/submit/successfull'], type='http', auth="public", website=True)
    def partner_form(self, **post):
        print('taest111111111111111111111111111')
        leaves_id = request.env['hr.leave.type'].sudo().search([])
        data = {
            'leaves_id': leaves_id,
        }
        print("emloyee form data 11", leaves_id)
        return request.render("odoocms_employee_portal.employee_leaves_form_submit", data)

    @http.route(['/leaves/form/submit'], type='http', auth="public", website=True)
    # next controller with url for submitting data from the form#
    def customer_form_submit(self, **post):
        print(12333232323232323333, post)
        # self.partner_form()
        holiday_status_id = post.get('leaves')
        date_from = post.get('date_from')
        date_to = post.get('date_to')
        name = post.get('name')
        duration_display = post.get('duration_display')
        print(5555555555555555555555, holiday_status_id)
        leave_request = request.env['hr.leave'].create({
            'holiday_status_id': holiday_status_id,
            'date_from': date_from,
            'date_to': date_to,
            'name': name,
            'duration_display': duration_display,
        })
        # inherited the model to pass the values to the model from the form#
        return request.render("odoocms_employee_portal.tmp_customer_form_success", leave_request)
        # finally send a request to render the thank you page#

    #
    # @http.route(['/leaves/form/submit'], type='http', auth="public", website=True)
    # def leaves_form_submit(self, **post):
    #     # holiday_status_id = Fields.Many2one('hr.leave.type', String="Type")
    #
    #     leaves_id = request.env['hr.leave.type'].sudo().search([])
    #     data = {
    #         'leaves_id': leaves_id,
    #     }
    #     print("emloyee form data 11", leaves_id)
    #     return request.render("odoocms_employee_portal.employee_leaves_form_submit", data)
    #
    # @http.route(['/leaves/form/submit/successfull'], type='http', auth="public", website=True)
    # def customer_form_submit(self, **post):
    #     print(11111111111111111, post)
    #     # contact_data = self.empp_submit(post)
    #     holiday_status_id = post.get('leaves')
    #     date_from = post.get('date_from')
    #     date_to = post.get('date_to')
    #     name = post.get('name')
    #     duration_display = post.get('duration_display')
    #     print(22222222222222222, holiday_status_id)
    #     leave_request = request.env['hr.leave'].create({
    #         'holiday_status_id': holiday_status_id,
    #         'date_from': date_from,
    #         'date_to': date_to,
    #         'name': name,
    #         'duration_display': duration_display,
    #     })
    #     print("emloyee form data2222222222222222222222222222222222233333333333333333222222222")
    #
    #     return request.render("odoocms_employee_portal.employee_leaves_form_submit", leave_request)

    # http.request.env['odoocms.application.preference'].sudo().create({
    #     'application_id': application.id,
    #     'program_id': int(kw.get('program_id')),
    #     'discipline_preference': discipline_preference,
    #     'preference': preference
    # })

    # def empp_submit(self, kw):
    #     return request.render("odoocms_employee_portal.tmp_customer_form_success", user)

    # leaves_id = request.env['hr.leave.type'].sudo().search([])
    # leaves_id = {
    #     'holiday_status_id': holiday_status_id,
    #     'date_from': date_from,
    #     'date_to': date_to,
    #     'name': name,
    #     'duration_display': duration_display,
    # }
    #
    # holiday_status_id = kw.get('holiday_status_id')
    # date_from = kw.get('date_from')
    # date_to = kw.get('date_to')
    # name = kw.get('name')
    # duration_display = kw.get('duration_display')
    #
    # print("emloyee form data 555555555555555555555555555555555555555555",holiday_status_id ,date_from)
    #
    #
    #
    # request.env['hr.leave.type'].sudo().create(leaves_id)
    #
    # print("emloyee form data444444444444444444444444444444444444444444444444444", leaves_id)
    #
    # return request.render("odoocms_employee_portal.tmp_customer_form_success", leaves_id)


class LeavesTypes(http.Controller):

    @http.route(['/leaves/types'], type='http', auth="user", website=True)
    def leaves_details(self, **kw):
        return request.render("odoocms_employee_portal.leave_tyes_form", )


class LeavesSummaryDetails(http.Controller):

    @http.route(['/leaves/summary/details'], type='http', auth="user", website=True)
    def leaves_form(self, **kw):
        current_user = http.request.env.user

        leaves_summary_id = request.env['hr.leave.allocation'].sudo().search([('employee_id', '=', current_user.name)])
        return request.render("odoocms_employee_portal.leaves_summary_details_template",
                              {'leaves_summary_id': leaves_summary_id,

                               }
                              )


class AnnualSummaryDetails(http.Controller):

    @http.route(['/annual/leaves/summary'], type='http', auth="user", website=True)
    def get_sales(self, ):
        current_user = http.request.env.user
        annual_leaves_id = http.request.env['hr.employee'].sudo().search([])
        # ('employee_id', '=', current_user.name)
        return request.render("odoocms_employee_portal.annual_leaves_summary_details_template",
                              {'annual_leaves_id': annual_leaves_id, })

    # annual_leaves_id = request.env['hr.leave.report'].sudo().search([])


class Employeedetails(http.Controller):

    @http.route(['/employee/main/details'], type='http', auth="user", website=True)
    def leaves_details(self, **kw):
        leaves_id = request.env['hr.employee'].sudo().search([])
        return "hello employees"

    # This is to download the report


class TestReport(http.Controller):

    def _show_report(self, model, report_type, report_ref, download=False):
        if report_type not in ('html', 'pdf', 'text'):
            raise UserError(_("Invalid report type: %s") % report_type)

    @http.route(['/employee/dashboard/page'], type='http', website=True)
    def employee_page(self, **kw):
        return request.render("odoocms_employee_portal.employee_portal_dashboard_page")
