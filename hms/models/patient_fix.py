from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class PatientFix(models.Model):
    _name = 'hms.patient.fix'
    _description = 'Fixed Patient'
    _rec_name = 'full_name'

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email must be unique!')
    ]

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    email = fields.Char(string="Email", required=True)  # <-- New email field
    birth_date = fields.Date(string="Birth Date", required=True)
    history = fields.Html(string="Medical History")
    cr_ratio = fields.Float(string="CR Ratio")
    blood_type = fields.Selection(
        [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
         ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        string="Blood Type",
        required=True
    )
    pcr = fields.Boolean(string="PCR Tested")
    image = fields.Image(string="Image")
    address = fields.Text(string="Address", required=True)
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    department_id = fields.Many2one(
        'hms.department',
        domain=[('is_opened', '=', True)],
        string="Department",
        required=True
    )
    doctor_ids = fields.Many2many(
        'hms.doctor',
        string="Doctors",
        domain="[('department_id', '=', department_id)]"
    )
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')
    full_name = fields.Char(string="Full Name", compute="_compute_full_name", store=True)
    show_history = fields.Boolean(string="Show History")
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Log History")

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = fields.Date.today()
                rec.age = today.year - rec.birth_date.year - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age = 0

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"

    @api.onchange('age')
    def _onchange_age(self):
        for rec in self:
            rec.show_history = rec.age >= 50
            if rec.age < 30:
                rec.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Automatically Checked',
                        'message': 'PCR has been automatically checked because age is below 30.'
                    }
                }

    @api.onchange('pcr', 'cr_ratio')
    def _onchange_pcr_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                return {
                    'warning': {
                        'title': 'CR Ratio Required',
                        'message': 'CR Ratio must be filled if PCR is checked.'
                    }
                }

    @api.constrains('email')
    def _check_valid_email(self):
        """Ensure email is in valid format."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        for record in self:
            if record.email and not re.match(pattern, record.email):
                raise ValidationError('Please enter a valid email address.')

    def write(self, vals):
        if 'email' in vals and vals['email']:
            vals['email'] = vals['email'].lower()

        res = super(PatientFix, self).write(vals)

        # Check if the state is being changed
        if 'state' in vals:
            new_state = vals.get('state')
            state_display = dict(self._fields['state'].selection).get(new_state)
            
            # Create a log entry whenever the state changes
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'created_by': self.env.user.id,
                'description': f"State changed to {state_display}",
            })

        return res

    @api.model
    def create(self, vals):
        if 'email' in vals and vals['email']:
            vals['email'] = vals['email'].lower()
        return super(PatientFix, self).create(vals)