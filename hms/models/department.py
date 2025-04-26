from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char(string="Department Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Is Opened", default=False)  # Default value is False
    doctor_ids = fields.Many2many(
        'hms.doctor', 'department_doctor_rel', 'department_id', 'doctor_id', string='Doctors'
    )
    patients = fields.One2many(
        'hms.patient', 'department_id', string='Patients'
    )
