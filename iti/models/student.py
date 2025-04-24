from odoo import models, fields

class Student(models.Model):
    _name = 'iti.student'
    _description = 'Student'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
