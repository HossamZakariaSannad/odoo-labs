from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Link to your fixed patient model
    related_patient_fix_id = fields.Many2one('hms.patient.fix', string='Related Fixed Patient')

    # Show Patient Name based on linked patient
    related_patient_fix_name = fields.Char(string='Patient Name', compute='_compute_related_patient_fix_name', store=True)

    vat = fields.Char(string='Tax ID')

    @api.depends('related_patient_fix_id')
    def _compute_related_patient_fix_name(self):
        for partner in self:
            partner.related_patient_fix_name = partner.related_patient_fix_id.full_name if partner.related_patient_fix_id else ''

    @api.constrains('related_patient_fix_id')
    def _check_related_patient_fix_email_unique(self):
        for record in self:
            if record.related_patient_fix_id:
                # Ensure no other CRM customer has the same email as the related patient's email
                domain = [
                    ('id', '!=', record.id),
                    ('type', '=', 'contact'),
                    ('related_patient_fix_id.email', '=', record.related_patient_fix_id.email)
                ]
                if self.search(domain, limit=1):
                    raise ValidationError('This patient email is already linked to another CRM customer.')

    @api.onchange('related_patient_fix_id')
    def _onchange_related_patient_fix(self):
        if self.related_patient_fix_id:
            self.email = self.related_patient_fix_id.email

    @api.constrains('vat', 'type')
    def _check_tax_id(self):
        for record in self:
            if (record.type == 'contact' or record.is_company) and not record.vat:
                raise ValidationError('Tax ID (VAT) is mandatory for CRM customers.')