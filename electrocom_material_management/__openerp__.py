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
    'name': 'Gestión MR Electrocom',
    'versiom': '8.0.0.1',
    'category': 'Mnufacturing',
    'summary': 'Gestión MR Electrocom',
    'author': 'Alexander Rodriguez <adtr271988@gmail.com>',
    'depends': ['base','report'],
    'application': True,
    'installable': True,
    'data':[
                'data/sequence.xml',
                'wizard/upload_wizard_view.xml',
                'electrocom_material_view.xml',
                'electrocom_material_import_view.xml',
                'electrocom_mr_view.xml',
                'views/report_mr.xml',
                'electrocom_report.xml',
            ],
}
