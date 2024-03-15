from odoo import http
from odoo.http import request
import base64



class WebsiteForm(http.Controller):
    @http.route(['/location'], type='http', auth="user", website=True)
    def employee_forms(self):
        partners = request.env['res.partner'].sudo().search([])
        values = {}
        values.update({
            'partners': partners
        })
        return request.render("location_search.online_employee_test", values)
#
class Location(http.Controller):
    @http.route('/location', type='http', auth="public",
                 website="True")
    def employee_test(self, **post):
        emp = request.env['hr.employee'].sudo().search([])
        values = {}
        values.update({
            'emp': emp[0]
        })
        return request.render("location_search.online_employee_test", values)
#

    @http.route("/contact-us", type="http", auth="user", website=True)
    def create_employee_details(self, **post):

        name = post.get('search')
        print(name)
#         email = post.get('email')
#         phone = post.get('phone')
#         gender = post.get('gender')
#         birthday = post.get('date_of_birth')
#         address = post.get('street')
#         father_name = post.get('father_name')
#         # print('post===', post)
#         data = post.get('att')
#         # doc_types = post.get('names')
#         file = post.get('filename')
#         # file11 = post.get('attachment')
#         # print('file11=====', file11)
#         type = post.get('type')
#
#
#
#         if name and email and phone and birthday:
#             employee = request.env['hr.employee'].sudo().create({
#                 'name': name,
#                 'contact_no': phone,
#                 'personal_email': email,
#                 'gender': gender,
#                 'birthday': birthday,
#                 'address': address,
#                 'father_name': father_name,
#                 # 'employee_attach_ids': [(0, 0, values)]
#             })
#             Attachment = request.env['ir.attachment']
#             file_name = post.get('att').filename
#             attachment_id = Attachment.create({
#                 'name': file_name,
#                 'type': 'binary',
#                 'datas': base64.b64encode(data.read()),
#                 'res_model': employee._name,
#                 'res_id': employee.id
#             })
#             values = {
#                 'name': name,
#                 'attachment': attachment_id.id,
#                 # 'types': type,
#             }
#             employee.update({
#                 'attachment': [(4, attachment_id.id)],  #(0, 0, values)]
#
#             })
#
#             return request.redirect('/employee/submit?submitted=1')
        return request.render('website_crm.contactus_form', {'submiitted': post.get('submitted', False)})



