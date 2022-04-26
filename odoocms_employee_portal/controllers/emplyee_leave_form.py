from odoo import http
from odoo.http import request

import io
import re

from PyPDF2 import PdfFileReader, PdfFileWriter

from odoo.http import request, route, Controller
from odoo.tools.safe_eval import safe_eval


class PartnerForm(http.Controller):

    @http.route(['/customer/form'], type='http', auth="public", website=True)
    def partner_form(self, **post):
        print("emloyee kanakkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkklllllllllllll New", post)

        leaves_id = request.env['hr.leave.type'].sudo().search([])
        data = {
            'leaves_id': leaves_id,
        }
        print("emloyee kanakkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkNeww", data)
        return request.render("odoocms_employee_portal.tmp_customer_form", data)

    @http.route(['/customer/form/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        request.env['hr.leave'].create({
            'leaves_id': post.get('leaves_id'),
            'date_from': post.get('date_from'),
            'date_to': post.get('date_to'),
            'name': post.get('name'),
            'duration_display': post.get('duration_display'),
        })
        return request.render("odoocms_employee_portal.tmp_customer_form_success")



class HrPayroll(Controller):

    @route(["/print/payslips"], type='http', auth='user')
    def get_payroll_report_print(self, list_ids='', **post):
        print("898989898989898989898989898989")

        if not request.env.user.has_group('odoocms_employee_portal.group_hr_payroll_user') or not list_ids or re.search(
                "[^0-9|,]", list_ids):
            return request.not_found()
        print("898989898989898989898989898989")


        ids = [int(s) for s in list_ids.split(',')]
        payslips = request.env['hr.payslip'].browse(ids)

        pdf_writer = PdfFileWriter()

        for payslip in payslips:
            if not payslip.struct_id or not payslip.struct_id.report_id:
                report = request.env.ref('odoocms_employee_portal.action_report_payslip', False)
            else:
                report = payslip.struct_id.report_id
            pdf_content, _ = report.render_qweb_pdf(payslip.id)
            reader = PdfFileReader(io.BytesIO(pdf_content), strict=False, overwriteWarnings=False)

            for page in range(reader.getNumPages()):
                pdf_writer.addPage(reader.getPage(page))

        _buffer = io.BytesIO()
        pdf_writer.write(_buffer)
        merged_pdf = _buffer.getvalue()
        _buffer.close()

        if len(payslips) == 1 and payslips.struct_id.report_id.print_report_name:
            report_name = safe_eval(payslips.struct_id.report_id.print_report_name, {'object': payslips})
        else:
            report_name = "Payslips"

        pdfhttpheaders = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(merged_pdf)),
            ('Content-Disposition', 'attachment; filename=' + report_name + '.pdf;')
        ]

        return request.make_response(merged_pdf, headers=pdfhttpheaders)
