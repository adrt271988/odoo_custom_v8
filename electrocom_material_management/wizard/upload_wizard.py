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

import os
import tempfile
import base64
import csv
from datetime import datetime
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError

class UploadMaterialWizard(models.TransientModel):
    _name = 'upload.material.wizard'

    def get_extension(self, filename):
        ext = str(os.path.basename(filename)).split('.', 1)[1]
        return '.' + ext if ext else None
    
    @api.one
    def upload_data(self):
        name = self.csv_filename
        if self.get_extension(name) != '.csv':
            raise ValidationError(_("La extensión del archivo debe ser .csv"))
        data = base64.decodestring(self.csv_file)
        fobj = tempfile.NamedTemporaryFile(delete=False)
        fname = fobj.name
        fobj.write(data)
        fobj.close()
        archive = csv.DictReader(open(fname))
        mto = self.env['electrocom.material.import'].browse(self._context['active_id'])
        lines = []
        for line in archive:
            lineValues = {}
            idItem = line.get('ID_ITEM',False)
            quantity = float(line.get('CANTIDAD',0.00))
            lineValues = dict(
                    name = idItem and idItem or '',
                    quantity = line.get('CANTIDAD',''),
                    description = line.get('DESCRIPCION',''),
                    tipo_mr = line.get('TIPO_MR','')
                )
            lines.append((0,0,lineValues))
        mto.lines = lines
        return {'type': 'ir.actions.act_window_close'}
        
    csv_file = fields.Binary(string='Archivo', required=True, filters='*.csv',
                    help="Seleccione un archivo de tipo csv para cargar los materiales")
    csv_filename = fields.Char(string="Nombre")
