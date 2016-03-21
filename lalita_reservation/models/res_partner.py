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
from openerp import models, fields, api, _

class LalitaResPartner(models.Model):
    _inherit = 'res.partner'

    guest_state = fields.Selection(
        [('draft','Nuevo'),
        ('confirmed','Confirmado'),
        ('canceled','Cancelado'),
        ('no_show','No Show'),
        ('check_in','Check in'),
        ('early_leave','Salida Temprana'),
        ('check_out','Check out'),],
        string='Estado del Huesped', index=True, default='draft',
        track_visibility='onchange', copy=False)
