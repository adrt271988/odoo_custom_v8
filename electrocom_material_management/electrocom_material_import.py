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
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError

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

    @api.one
    def update_master(self):
        master_obj = self.env['electrocom.material']
        record = False
        for line in self.lines:
            values = {}
            master = master_obj.search([('name','=',line.name)])
            if master:
                master.quantity += line.quantity
            else:
                idItem = line.name
                values = dict(
                    name = idItem and idItem or '',
                    quantity = line.quantity,
                    description = line.description,
                    tipo_mr = line.tipo_mr,
                    discipline = idItem and idItem.split("-")[0] or '',
                    discipline_type = idItem and idItem.split("-")[1] or '',
                    code = idItem and idItem.split("-")[2] or '',
                    import_id = self.id
                )
                record = master_obj.create(values)
        if record:
            self.state = 'done'
        else:
            ValidationError(_("Error al actualizar el maestro de materiales"))

    @api.one
    def validate(self):
        if not self.lines:
            raise ValidationError(_("No es posible confirmar debido a que no se ha realizado ninguna importación"))
        self.state = 'open'

    @api.one
    def cancel_document(self):
        self.state = 'cancel'

    @api.one
    def create_mr(self):
        if self.lines:
            self.env.cr.execute('SELECT tipo_mr FROM electrocom_material_import_line \
                                        WHERE import_id = %d GROUP BY tipo_mr'%self.id)
            result = self.env.cr.fetchall()
            for res in result:
                mr_lines = []
                importLines = self.lines.search([('tipo_mr','=',res[0])])
                for il in importLines:
                    lineVals = {}
                    material = self.env['electrocom.material'].search([('name','=',il.name)])
                    lineVals = dict(
                        material_id = material and material.id or '',
                        id_item = material and material.name or il.name,
                        description = material and material.description or il.description,
                        unit = material and material.measurement_unit or '',
                        quantity = il.quantity)
                    mr_lines.append((0,0,lineVals))
                self.env['electrocom.mr'].create(dict(
                    name = self.project_code+'-MR-'+res[0],
                    mr_lines = mr_lines))
        self.mr_exists = True
    
    @api.model
    def create(self, values):
        if not values.get('sequence'):
            values['sequence'] = self.env['ir.sequence'].get('electrocom.material.import')
        return super(ElectrocomMaterialImport, self).create(values)

    sequence = fields.Char(string='Secuencia', readonly=True)
    project_code = fields.Char(string="Proyecto", help="Código del Proyecto")
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
    tipo_mr = fields.Char(string="TIPO MR")
    import_id = fields.Many2one('electrocom.material.import')
