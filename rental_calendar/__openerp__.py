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
    'name': 'Calendario para Alquileres',
    'category': '', 
    'version': '1.0',
    'description': """ 
Calendario para Alquileres
====================================================
* Calendarizar los alquileres y movimientos de stock que se generan
* Filtros por pedido y cliente en listado de Alquileres
* Envio de correos y notificaciones a los clientes sobre los alquileres por vencer
* Facturar al cliente por pérdidas de articulos alquilados
    """,
    'author': 'Alexander Rodriguez (adrt271988@gmail.com)',
    'website': '',
    'depends': ['sale_rental'],
    'data': [
            'stock_move.xml',
            'rental_view.xml',
            'product_view.xml',
            'email_template.xml',
            'ir_cron.xml',
            'wizard/rental_invoice_missing.xml',
            'sale_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
