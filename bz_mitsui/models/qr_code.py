# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models, _
from odoo.http import request
import datetime
from odoo.exceptions import ValidationError

try:
   import qrcode
except ImportError:
   qrcode = None
try:
   import base64
except ImportError:
   base64 = None
from io import BytesIO

class ReportInvoice(models.Model):
   _inherit = "project.project"

   qr_code = fields.Binary('QRcode', compute="_generate_qr")
   nabl = fields.Binary('Nabl', compute="_generate_nabl")

   def _generate_qr(self):
       "method to generate QR code"
       for rec in self:
           if qrcode and base64:
               qr = qrcode.QRCode(
                   version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=3,
                   border=4,
               )
               base_url = self.env['ir.config_parameter'].get_param('web.base.url')
               qr.add_data(base_url)
               print(base_url)
               qr.make(fit=True)
               img = qr.make_image()
               temp = BytesIO()
               img.save(temp, format="PNG")
               qr_image = base64.b64encode(temp.getvalue())
               rec.update({'qr_code':qr_image})

   def _generate_nabl(self):
       "method to generate QR code"
       for rec in self:
           if qrcode and base64:
               nabl1 = qrcode.QRCode(
                   version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=3,
                   border=4,
               )

               nabl1.add_data('nablwp.qci.org.in')
               nabl1.make(fit=True)
               img1 = nabl1.make_image()
               temp = BytesIO()
               img1.save(temp, format="PNG")
               qr_image1 = base64.b64encode(temp.getvalue())
               rec.update({'nabl':qr_image1})