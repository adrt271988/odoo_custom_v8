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

    @api.model
    def create(self, values):
        if not values.get('sequence'):
            values['sequence'] = self.env['ir.sequence'].get('electrocom.mr')
        return super(ElectrocomMr, self).create(values)

    name = fields.Char(string='Código')
    sequence = fields.Char(string='Secuencia', readonly=True)
    notes = fields.Text(string='Notas')
    date_mr = fields.Datetime('Fecha de MR', default = lambda self: datetime.today())
    mr_lines = fields.One2many('electrocom.mr.line','material_id',string="Líneas MR")
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange', readonly=True,
            default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Compañía', change_default=True, readonly=True,
            default=lambda self: self.env['res.company']._company_default_get('electrocom.mr'))

class ElectrocomMrLine(models.Model):
    _name = 'electrocom.mr.line'
    _description = "Lineas MR"
    _order = "id asc"

    material_id = fields.Many2one('electrocom.material',string="Material")
    id_item = fields.Char(string="Id Item")
    description = fields.Char(string="Descripción")
    mr_id = fields.Many2one('electrocom.mr',string="MR")
    quantity= fields.Float(string="Cantidad")
    unit = fields.Char(strinf="Unidad Medidad")
