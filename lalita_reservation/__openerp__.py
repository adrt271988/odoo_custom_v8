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
    'depends': ['base'],
    'application': True,
    'installable': True,
    'data':[
                #~ 'views/bed_view.xml',
                'views/lalita_reservation_view.xml',
                'views/traveler_register_view.xml',
                #~ 'views/room_view.xml',
                #~ 'views/huespedes_view.xml',
            ],
}
