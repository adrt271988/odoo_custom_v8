# -*- encoding: utf-8 -*-
{
    'name': 'Secuencias Documentos',
    'version': '8.0.1',
    'category': 'Accounting',
    'summary': """Secuencias de documentos personalizadas en el Partner""",
    'description': """Secuencias de documentos personalizadas en el Partner""",
    'author': 'Alexander Rodriguez <adrt271988@gmail.com>',
    'depends': ['l10n_es_account_invoice_sequence','sale','purchase'],
    'init_xml': [],
    'data': [
        'res_partner_view.xml',
        'ir_sequence_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'demo_xml': [],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
