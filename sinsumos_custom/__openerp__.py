# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Módulo Personalizado Sinsumos',
    'version': '0.1',
    'description': """
Módulo Personalizado Sinsumos
====================================================================
* Incluye las modificaciones para la empresa Sinsumos
* Modificación de formatos de Facturas y Albaránes
* Descuentos globales en facturas de venta
* Configuración sencilla de conceptos básicos de Nómina Venezolana
    """,
    'author': 'Alexander Rodriguez',
    'website': '',
    'depends': ['base','account','sale_discount_total'],
    'data': [
            'data/res_country_state.xml',
            'views/report_invoice.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
