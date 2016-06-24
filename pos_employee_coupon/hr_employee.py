#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval


class EmployeeCouponHrEmployee(osv.osv):
    
    _inherit = 'hr.employee'

    def onchange_user(self, cr, uid, ids, user_id, context=None):
        res = super(EmployeeCouponHrEmployee, self).onchange_user(cr, uid, ids, user_id, context=None)
        if res and user_id:
            user_obj = self.pool.get('res.users')
            user_brw = user_obj.browse(cr, uid, user_id, context=context)
            if user_brw.partner_id:
                res['value'].update({'address_home_id': user_brw.partner_id.id})
        return res
