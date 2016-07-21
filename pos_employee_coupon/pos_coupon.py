# -*- coding: utf-8 -*-
##############################################################################
#
#    Custom module for Odoo
#    @author Onawoo Soluciones C.A.
#       Alexander Rodriguez <adrt271988@gmail.com>
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

from lxml import etree
from datetime import datetime
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')

class PosCoupon(models.Model):
    _name = 'pos.coupon'
    _description = "Employee Coupons"
    #~ _inherit = ['mail.thread']
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char(string="Código de Vale",select=True, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Empleado', required=True)
    order_id = fields.Many2one('pos.order', string='Pedido', required=True)
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange',
            default=lambda self: self.env.user)
    date = fields.Date(string='Fecha', required=True, default=lambda self: fields.Date.today())
    state = fields.Selection(
        [('draft','Sin Procesar'),
        ('done','Contabilizado')],
        string='Estatus',index=True, default='draft',
        track_visibility='onchange', copy=False)
    amount = fields.Float(string="Monto", required=True)

    @api.model
    def create(self, values):
        if not values.get('name'):
            values['name'] = self.env['ir.sequence'].get('pos.coupon')
        return super(PosCoupon, self).create(values)
