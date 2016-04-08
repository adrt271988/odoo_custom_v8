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
    'name': 'Lalita Registro de Viajeros',
    'versiom': '8.0.0.1',
    'category': 'Travel',
    'summary': 'Registro para Viajeros',
    'description': 'Gestión del Registro de Viajeros y envío de los partes a la Guardia Civil',
    'author': 'Jeronimo Spotorno, Alexander Rodriguez <adtr271988@gmail.com>',
    'depends': ['base','document','mail','sales_crm_custom','document_url'],
    'application': True,
    'installable': True,
    'data':[
                'data/lalita_reservation_sequence.xml',
                'views/res_partner_view.xml',
                'views/traveler_register_view.xml',
                'views/lalita_reservation_view.xml',
                'report/report_traveler_register.xml',
                'lalita_reservation_report.xml',
                'data/email_template.xml',
            ],
}
