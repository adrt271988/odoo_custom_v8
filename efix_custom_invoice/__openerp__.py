# -*- encoding: utf-8 -*-
##############################################################################
#
#    Custom module for Odoo
#    @author Alexander Rodriguez <adrt271988@gmail.com>
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
    'name': 'Factura Personalizada EFix',
    'versiom': '8.0.0.1',
    'category': 'Accounting',
    'summary': 'Factura Personalizada Efix',
    'description': 'Formato personalizado de Facturas para Efix',
    'author': 'Alexander Rodriguez <adtr271988@gmail.com>',
    'depends': ['base','report','account'],
    'application': True,
    'installable': True,
    'data':[
                'view/report_invoice.xml',
            ],
}
