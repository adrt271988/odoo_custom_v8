# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp.osv import fields,osv

class calendar_event_inherit(osv.osv):
    _inherit = 'calendar.event'

    def _get_partner_ids(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        lawyers = []
        clients = []
        employees = []
        for calendar in self.browse(cr, uid, ids, context=context):
            if calendar.lawyer_ids:
                lawyers = [x.id for x in calendar.lawyer_ids]
            if calendar.client_ids:
                clients = [x.id for x in calendar.client_ids]
            if calendar.lawyer_ids:
                employees = [x.id for x in calendar.employee_ids]
            res[calendar.id] = lawyers + clients + employees
        return res

    _columns = {
        'lawyer_ids': fields.many2many('res.partner', 'calendar_event_res_partner_lawyer_rel', string='Lawyers', states={'done': [('readonly', True)]}),
        'client_ids': fields.many2many('res.partner', 'calendar_event_res_partner_client_rel', string='Clients', states={'done': [('readonly', True)]}),
        'employee_ids': fields.many2many('res.partner', 'calendar_event_res_partner_employee_rel', string='Employees', states={'done': [('readonly', True)]}),
        #~ 'partner_ids': fields.function(_get_partner_ids, type='many2many', relation="res.partner", string="Attendees", store=True),

    }
