# -*- coding: utf-8 -*-
{
    'name': 'PoS Invoice Ticket',
    'version': '1.0',
    'category': 'Point Of Sale',
    'summary': 'Print Invoice as ticket in Point of Sale',
    'description': """
Main Features
-------------
* Add a new button to print invoice as ticket in Point of Sale
    """,
    'author': 'Jose Suniaga <suniagajose@gmail.com>',
    'depends': ['point_of_sale', 'tg_pos_debt_notebook', 'partner_employee'],
    'data': [
        'views/view.xml'
    ],
    'qweb': [
        'static/src/xml/invoice.xml',
    ],
    'installable': True,
    'auto_install': False,
}