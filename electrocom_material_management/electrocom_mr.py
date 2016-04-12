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

class ElectrocomMr(models.Model):
    _name = 'electrocom.mr'
    _description = "MRs"
    _order = "id asc"
    _rec_name = "name"

    name = fields.Char(string='Código')
    notes = fields.Text(string='Notas')
    mr_lines = fields.One2many('electrocom.mr.line','material_id',string="Líneas MR")

class ElectrocomMrLine(models.Model):
    _name = 'electrocom.mr.line'
    _description = "Lineas MR"
    _order = "id asc"

    material_id = fields.Many2one('electrocom.material',string="Material")
    mr_id = fields.Many2one('electrocom.mr',string="MR")
    quantity= fields.Float(string="Cantidad")
