from odoo import fields, models


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    check_in_latitude = fields.Float(
        "Check-in Latitude", digits="Location", readonly=True
    )
    check_in_longitude = fields.Float(
        "Check-in Longitude", digits="Location", readonly=True
    )
    check_out_latitude = fields.Float(
        "Check-out Latitude", digits="Location", readonly=True
    )
    check_out_longitude = fields.Float(
        "Check-out Longitude", digits="Location", readonly=True
    )

    check_in_location = fields.Char(string="Check in Location")
    check_out_location = fields.Char(string="Check out Location")

