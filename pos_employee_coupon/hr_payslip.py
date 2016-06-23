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
from openerp import api, tools, models, fields, _
#~ from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval


class EmployeeCouponHrPayslip(models.Model):
    
    _inherit = 'hr.payslip'

    @api.multi
    @api.depends('employee_id','date_from','date_to')
    def _get_coupon_amount(self):
        for payslip in self:
            pos_coupon = self.env['pos.coupon'].search([('employee_id','=',payslip.employee_id.id),('date','>=',payslip.date_from),('date','<=',payslip.date_to)])
            if pos_coupon:
                payslip.coupon_amount = sum([x.amount for x in pos_coupon])

    coupon_amount = fields.Float('Total Vales', compute='_get_coupon_amount', help="Total vales del período de la Nómina")
