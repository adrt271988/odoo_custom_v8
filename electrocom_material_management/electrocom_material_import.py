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

    @api.multi
    def upload_data(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        view_form = self.env.ref('electrocom_material_management.upload_material_form', False)
        return {
            'name': _('Importar Data'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'upload.material.wizard',
            'views': [(view_form.id, 'form')],
            'view_id': view_form.id,
            'target': 'new'
        }
    
    @api.model
    def create(self, values):
        if not values.get('sequence'):
            values['sequence'] = self.env['ir.sequence'].get('electrocom.material.import')
        return super(ElectrocomMaterialImport, self).create(values)

    sequence = fields.Char(string='Secuencia', readonly=True)
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange', readonly=True,
            default=lambda self: self.env.user)
    import_date = fields.Datetime('Fecha de Importación', default = lambda self: datetime.today())
    lines = fields.One2many('electrocom.material.import.line','import_id','Detalle')
    mr_exists = fields.Boolean(string = 'Existe MR asociada', default=False)
    state = fields.Selection(
        [('draft','Borrador'),
        ('open','Confirmado'),
        ('cancel','Cancelado'),
        ('done','Finalizado')],
        string='Estatus',index=True, default='draft',
        track_visibility='onchange', copy=False)

class ElectrocomMaterialImportLine(models.Model):
    _name = "electrocom.material.import.line"
    _description = "Detalle Importacion de Materiales"
    _order = "id asc"

    name = fields.Char(string='ID_ITEM', size=15)
    description = fields.Char(string='DESCRIPCIÓN')
    quantity = fields.Float(string="CANTIDAD")
    import_id = fields.Many2one('electrocom.material.import')
