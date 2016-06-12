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
from openerp.osv import osv
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')

class PosOrderInherit(osv.osv):
    _inherit = 'pos.order'
    
    def create(self, cr, uid, values, context=None):
        order_id = super(PosOrderInherit, self).create(cr, uid, values, context=context)
        order = self.browse(cr, uid, order_id, context = context)
        coupon = self.pool.get('pos.coupon')
        user_obj = self.pool.get('res.users')
        employee_obj = self.pool.get('hr.employee')
        user_id = user_obj.search(cr, uid, [('partner_id','=',order.partner_id.id)])
        if user_id:
            employee_id = employee_obj.search(cr, uid, [('user_id','=',user_id[0]))
        return order_id
