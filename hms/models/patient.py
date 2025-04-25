from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'full_name'  # Set the display name as the full_name field

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    birth_date = fields.Date(string="Birth Date")
    history = fields.Html(string="Medical History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), 
         ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        string="Blood Type"
    )
    pcr = fields.Boolean(string="PCR Tested")
    image = fields.Image(string="Image")
    address = fields.Text(string="Address")
    age = fields.Integer(string="Age")
    department_id = fields.Many2one('hms.department')
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    # Define a computed field for full name
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"


# Add onchange for age
    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Automatically Checked',
                    'message': 'PCR has been automatically checked because age is below 30.'
                }
            }

# Make cr_ratio required if PCR checked
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required if PCR is checked.")

# Prevent assigning to closed department
    @api.constrains('department_id')
    def _check_department_open(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("Cannot assign patient to a closed department.")

