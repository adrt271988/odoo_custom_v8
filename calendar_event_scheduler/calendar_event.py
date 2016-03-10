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
from datetime import datetime, timedelta
from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from openerp import tools, SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _

class calendar_event_inherit(osv.osv):
    _inherit = 'calendar.event'

    def toDatetime(self, cr, uid, dateString, context=None):
        if len(dateString) == 10:
            dateString+=" 00:00:00"
        return datetime.strptime(dateString, DEFAULT_SERVER_DATETIME_FORMAT)

#  
#  name: calendar_event_inherit.check_availability
#  @param: recibe lista de partners a verificar en otros eventos, fecha inicio y fecha fin
#  @return: regresa un diccionario con elementos de warning de onchange o diccionario vacio
#  
    def check_availability(self, cr, uid, partners, start, end, context = None):
        warning = {}
        calendar_ids = self.search(cr, uid, [])
        calendar_brw = self.browse(cr, uid, calendar_ids, context)
        flag = False
        for calendar in calendar_brw:
            att = [x.id for x in calendar.partner_ids]
            match = [x for x in partners if x in att]
            if match:
                if start:
                    if self.toDatetime(cr, uid, calendar.start) == self.toDatetime(cr, uid, start):
                        flag = True
                if end:
                    if self.toDatetime(cr, uid, calendar.stop) == self.toDatetime(cr, uid, end):
                        flag = True
        if flag:
            warning.update({'message': _("At least one attendee of the list is already booked for that date or time!"),'title': _('Attendee already booked')})
        return warning
        
    def onchange_dates(self, cr, uid, ids, fromtype, partner_ids = False, start=False, end=False, checkallday=False, allday=False, context=None):
        """Returns duration and end date based on values passed
        @param ids: List of calendar event's IDs.
        """
        value = {}

        if checkallday != allday:
            return value

        if partner_ids and partner_ids[0][2]:
            warning = self.check_availability(cr, uid, partner_ids[0][2], start, end, context = context)
            if warning:
                value.update({'warning':warning})
                return value

        value['allday'] = checkallday  # Force to be rewrited

        if allday:
            if fromtype == 'start' and start:
                start = datetime.strptime(start, DEFAULT_SERVER_DATE_FORMAT)
                value['start_datetime'] = datetime.strftime(start, DEFAULT_SERVER_DATETIME_FORMAT)
                value['start'] = datetime.strftime(start, DEFAULT_SERVER_DATETIME_FORMAT)

            if fromtype == 'stop' and end:
                end = datetime.strptime(end, DEFAULT_SERVER_DATE_FORMAT)
                value['stop_datetime'] = datetime.strftime(end, DEFAULT_SERVER_DATETIME_FORMAT)
                value['stop'] = datetime.strftime(end, DEFAULT_SERVER_DATETIME_FORMAT)

        else:
            if fromtype == 'start' and start:
                start = datetime.strptime(start, DEFAULT_SERVER_DATETIME_FORMAT)
                value['start_date'] = datetime.strftime(start, DEFAULT_SERVER_DATE_FORMAT)
                value['start'] = datetime.strftime(start, DEFAULT_SERVER_DATETIME_FORMAT)
            if fromtype == 'stop' and end:
                end = datetime.strptime(end, DEFAULT_SERVER_DATETIME_FORMAT)
                value['stop_date'] = datetime.strftime(end, DEFAULT_SERVER_DATE_FORMAT)
                value['stop'] = datetime.strftime(end, DEFAULT_SERVER_DATETIME_FORMAT)

        return {'value': value}
    
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

    def create(self, cr, uid, vals, context=None):
        if 'partner_ids' in vals and 'start' in vals and 'stop' in vals:
            warning = self.check_availability(cr, uid, vals['partner_ids'][0][2], vals['start'], vals['stop'], context = context)
            if warning:
                raise osv.except_osv(warning['title'],warning['message'])
        return super(calendar_event_inherit, self).create(cr, uid, vals, context = context)
