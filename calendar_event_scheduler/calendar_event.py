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

    def check_partners_availability(self, cr, uid, partner_ids, context=None):
        partner_obj = self.pool.get('res.partner')
        return True
    
    def onchange_attendee_ids(self, cr, uid, ids, lawyers, clients, employees, context=None):
        res = {'value': {}}
        if not lawyers and not clients and not employees:
            return
        attendees = []
        if lawyers and lawyers[0][2]:
            attendees+=lawyers[0][2]
        if clients and clients[0][2]:
            attendees+=clients[0][2]
        if employees and employees[0][2]:
            attendees+=employees[0][2]
        res['value'] = {'partner_ids':[(6,0,attendees)]}
        return res

    _columns = {
        'lawyer_ids': fields.many2many('res.partner', 'calendar_event_res_partner_lawyer_rel',
                                            string='Lawyers', states={'done': [('readonly', True)]}),
        'client_ids': fields.many2many('res.partner', 'calendar_event_res_partner_client_rel',
                                            string='Clients', states={'done': [('readonly', True)]}),
        'employee_ids': fields.many2many('res.partner', 'calendar_event_res_partner_employee_rel',
                                            string='Employees', states={'done': [('readonly', True)]}),
    }
