from odoo import models, fields, api

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'
    _rec_name = 'full_name'

    full_name = fields.Char(compute='_compute_full_name', store=True)
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Image()
    
    patients = fields.Many2many('hms.patient')


    department_id = fields.Many2one('hms.department', string='Department')

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"
