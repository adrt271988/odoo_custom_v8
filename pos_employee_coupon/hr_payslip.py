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

class EmployeeCouponResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def _get_debt(self):
        """ Se hereda este método para disminuir la deuda al contabilizar los vales del empleado"""
        debt_account = self.env['account.account'].search([
            ('company_id', '=', self.env.user.company_id.id), ('code', '=', 'XDEBT')])
        debt_journal = self.env['account.journal'].search([
            ('company_id', '=', self.env.user.company_id.id), ('debt', '=', True)])

        self._cr.execute(
            """SELECT l.partner_id, SUM(l.debit - l.credit)
            FROM account_move_line l
            WHERE l.account_id = %s AND l.partner_id IN %s
            GROUP BY l.partner_id
            """,
            (debt_account.id, tuple(self.ids)))

        res = {}
        for partner in self:
            res[partner.id] = 0
        for partner_id, val in self._cr.fetchall():
            res[partner_id] += val

        statements = self.env['account.bank.statement'].search(
            [('journal_id', '=', debt_journal.id), ('state', '=', 'open')])
        if statements:

            self._cr.execute(
                """SELECT l.partner_id, SUM(l.amount)
                FROM account_bank_statement_line l
                WHERE l.statement_id IN %s AND l.partner_id IN %s
                GROUP BY l.partner_id
                """,
                (tuple(statements.ids), tuple(self.ids)))
            for partner_id, val in self._cr.fetchall():
                employee = self.env['hr.employee'].search([('address_home_id','=',partner_id)])
                coupons_amount = 0.00
                if employee:
                    pos_coupon = self.env['pos.coupon'].search([('employee_id','=',employee.id),
                                                        ('state','=','done')])
                    coupons_amount = sum([x.amount for x in pos_coupon])
                res[partner_id] += val - coupons_amount
        for partner in self:
            partner.debt = res[partner.id]

class EmployeeCouponHrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    @api.depends('employee_id','date_from','date_to')
    def _get_coupon_amount(self):
        for payslip in self:
            pos_coupon = self.env['pos.coupon'].search([('employee_id','=',payslip.employee_id.id),
                                                        ('date','>=',payslip.date_from),
                                                        ('date','<=',payslip.date_to),
                                                        ('state','=','draft')
                                                        ])
            if pos_coupon:
                payslip.coupon_amount = sum([x.amount for x in pos_coupon])

    coupon_amount = fields.Float('Total Vales', compute='_get_coupon_amount', help="Total vales del período de la Nómina")
        
    def compute_sheet(self, cr, uid, ids, context=None):
        slip_line_pool = self.pool.get('hr.payslip.line')
        sequence_obj = self.pool.get('ir.sequence')
        for payslip in self.browse(cr, uid, ids, context=context):
            number = payslip.number or sequence_obj.get(cr, uid, 'salary.slip')
            #delete old payslip lines
            old_slipline_ids = slip_line_pool.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)
#            old_slipline_ids
            if old_slipline_ids:
                slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
            if payslip.contract_id:
                #set the list of contract for which the rules have to be applied
                contract_ids = [payslip.contract_id.id]
            else:
                #if we don't give the contract, then the rules to apply should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to, context=context)
            lines = [(0,0,line) for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context)]
            for l in lines:
                line = l[2]
                if line.get('code') == 'VALE':
                    partner = payslip.employee_id.address_home_id
                    res = partner.debt + line.get('amount') #Viene negativo
                    coupon_obj = self.pool.get('pos.coupon')
                    coupon_ids = coupon_obj.search(cr, uid, [('employee_id','=',payslip.employee_id.id),
                                                        ('date','>=',payslip.date_from),
                                                        ('date','<=',payslip.date_to),
                                                        ('state','=','draft')
                                                        ])
                    coupon_obj.write(cr, uid, coupon_ids, {'state':'done'})
            self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number,}, context=context)
        return True
