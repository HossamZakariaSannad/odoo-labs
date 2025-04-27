# __manifest__.py
{
    'name': 'Hospital Management System',
    'version': '1.0',
    'category': 'Health',
    'author': 'Hossam',
    'depends': ['base'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/hms_security.xml',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/patient_fix.xml',  # Moved up to define menu_hms_fix
        'views/doctor_views.xml',
        'views/patient_log_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
}