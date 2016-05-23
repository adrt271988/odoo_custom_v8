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
from openerp import api, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval

days_schedule_pay = {
        'monthly': 30,
        'quarterly': 90,
        'semi-annually': 180,
        'annually': 365,
        'weekly': 7,
        'bi-weekly': 15,
        'bi-monthly': 60,
    }

class l10n_ve_hr_payslip(osv.osv):

    def onchange_contract_id(self, cr, uid, ids, date_from, date_to, employee_id=False, contract_id=False, context=None):
        res = super(l10n_ve_hr_payslip, self).onchange_contract_id(cr, uid, ids, date_from,\
                        date_to, employee_id, contract_id, context=context)
        if "value" in res:
            if "contract_id" in res['value']:
                contract_id = res['value']['contract_id']
                contract_brw = self.pool.get('hr.contract').browse(cr, uid, contract_id, context=context)
                period_days = days_schedule_pay.get(contract_brw.schedule_pay)
                if period_days:
                    date = time.strftime('%Y-%m-01')
                    date_from = datetime.strptime(date, "%Y-%m-%d")
                    end_date = date_from + timedelta(days=(period_days - 1))
                    res['value'].update({'date_to':end_date})
        return res

    _inherit = 'hr.payslip'
    _columns = {
        'mondays':fields.integer('N° de Lunes', required=True, help="Cantidad de Lunes del Periodo,\
                                                                usados para el cálculo de Retenciones SSO y Paro Forzoso"),
    }
