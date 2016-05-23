# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    $Id: account.py 1005 2005-07-25 08:41:42Z nicoe $
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "TXT de Recibos POS ",
    "version": "1.1",
    "author" : "",
    "category": "POS",
    "description":
    """
     Este modulo permite crear un txt para impresión o almacenamiento de los recibos de caja del módulo POS:
    """,
    'images': [],
    'depends': ['account','point_of_sale'],
    'data': [
             #'view/receipt_txt_conf.xml',
             'wizard/receipt_txt_view.xml',
            ],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': True,
    'auto_install': False,
}
