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

class LeavingMotive(models.TransientModel):
    _name = 'leaving.motive'
    
    @api.one
    def set_motive(self):
        guest_id = self._context['active_id']
        guest = self.env['lalita.guest'].browse(guest_id)
        guest.leaving_motive = self.motive
        return {'type': 'ir.actions.act_window_close'}
        
    motive = fields.Text(string="Motivo de Salida")
