# __manifest__.py
{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Health',
    'author': 'Hossam',
    'depends': ['base'],
    'data': [
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/patient_log_views.xml',
        'views/patient_fix.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
}
