from odoo import models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def attendance_manual(self, next_action, entered_pin=False, location=False):
        res = super(
            HrEmployee, self.with_context(attendance_location=location)
        ).attendance_manual(next_action, entered_pin)
        return res

    def _attendance_action_change(self):
        res = super()._attendance_action_change()
        location = self.env.context.get("attendance_location", False)
        employee_user = self.env['hr.employee'].search([('user_id','=', self.env.uid)], limit=1)
        if employee_user:
            attend_ids = self.env['hr.attendance'].search([('employee_id', '=', employee_user.id)])
            for attend in attend_ids:
                if self.attendance_state == "checked_in":
                    attend.check_in_location = 'http://maps.google.com/maps?q=' + str(location[0]) + ',' + str(location[1])
                else:
                    attend.check_out_location = 'http://maps.google.com/maps?q=' + str(location[0]) + ',' + str(location[1])
        if location:
            if self.attendance_state == "checked_in":
                res.write(
                    {
                        "check_in_latitude": location[0],
                        "check_in_longitude": location[1],
                    }
                )
            else:
                res.write(
                    {
                        "check_out_latitude": location[0],
                        "check_out_longitude": location[1],
                    }
                )
        return res
