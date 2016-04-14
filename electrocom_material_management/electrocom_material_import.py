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

class ElectrocomMaterialImport(models.Model):
    _name = 'electrocom.material.import'
    _description = "Importacion de Materiales"
    _order = "id asc"
    _rec_name = "sequence"

    sequence = fields.Char(string='Secuencia', size=4)
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange',
            default=lambda self: self.env.user)
    import_date = fields.Datetime('Fecha de Importación', default = lambda self: fields.Date.context_today(self))
