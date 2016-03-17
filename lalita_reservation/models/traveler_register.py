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
from openerp import models, fields

class TravelerRegister(models.Model):
    _name = 'traveler.register'
    _description = "Traveler Registration"
    _order = "id desc"
    _rec_name = "doc_number"
    
    doc_number = fields.Char('Documento Identificación', size=14,required=True,help="Número de Documento de Identidad")
    doc_type = fields.Selection(
            [('D','DNI Españoles'),
            ('P','Pasaportes'),
            ('C ','Permiso de conducir español'),
            ('I','Carta o documento de identidad'),
            ('X','Permiso de residencia UE'),
            ('N','Permiso de residencia español')],
            'Tipo de Documento', size=1, required=True)
    date_due = fields.Date('Fecha de Expedición', required=True)
    last_name1 = fields.Char('Primer Apellido', size=30, required=True)
    last_name2 = fields.Char('Segundo Apellido', size=30, required=True)
    first_name = fields.Char('Nombre', size=30, required=True)
    gender = fields.Selection([('F','Femenino'),('M','Masculino')],'Sexo',size=1,required=True)
    birth_date = fields.Date('Fecha de Nacimiento', required=True)
    birth_country = fields.Char('Pais de Nacionalidad', size=21, required=True)
    entry_date = fields.Date('Fecha de Entrada', required=True)
    sent = fields.Boolean('Enviado?', default=False)
