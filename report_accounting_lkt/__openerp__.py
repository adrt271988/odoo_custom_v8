# -*- encoding: utf-8 -*-
{
    'name': 'Reportes Contables LKTROKOM',
    'version': '0.1',
    'category': 'Accounting',
    'summary': """Reportes Contables Personalizados Electrocom""",
    'description': """Reportes Contables Personalizados Electrocom""",
    'author': 'Electrocom <adrt271988@gmail.com>',
    'depends': ['account'],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'wizard/accounting_reports_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'demo_xml': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
