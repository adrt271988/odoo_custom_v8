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

from datetime import datetime
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')

class ElectrocomMaterial(models.Model):
    _name = 'electrocom.material'
    _description = "Materiales"
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char(string='ID_ITEM', size=14, required=True)
    code = fields.Char(string='CODIGO', size=4, required=True)
    discipline = fields.Char(string='DISCIPLINA', size=3, required=True)
    discipline_type = fields.Char(string='TIPO DE DISCIPLINA', size=5, required=True)
    description = fields.Char(string='DESCRIPCIÓN', required=True)
    material_type_id = fields.Char(string='ID-TIPO PRODUCTO', size=1, required=True)
    cost_center_id = fields.Char(string='ID-CENTRO COSTO')
    manufacturer = fields.Char(string="MANUF") 
    account = fields.Char(string="CTA_CONTABLE")
    piping = fields.Char(string="ID PIPING")
