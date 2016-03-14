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
from dateutil.relativedelta import relativedelta
from openerp import tools, SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.tools.translate import _

class inherit_sale_order(osv.osv):
    _inherit = 'sale.order'

    def _get_field_by_lead(self, cr, uid, context=None):
        if context is None:
            context = {}
        lead_obj = self.pool.get('crm.lead')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False
        lead = lead_obj.read(cr, uid, [active_id], ['arrival_date','departure_date','berths'], context=context)
        return lead and lead[0] or False

    _columns = {
        'arrival_date': fields.datetime('Fecha de LLegada', help="Fecha de LLegada"),
        'departure_date': fields.datetime('Fecha de Salida', help="Fecha de Salida"),
        'berths': fields.integer('Número de Plazas',help="Número de Plazas"),
        'exclusive': fields.boolean('Exclusivo',help="Exclusivo"),
        'lead_id': fields.many2one('crm.lead','Oportunidad'),
    }

    _defaults = {
        'arrival_date': lambda self, cr, uid, context: self._get_field_by_lead(cr, uid, context)['arrival_date'],
        'departure_date': lambda self, cr, uid, context: self._get_field_by_lead(cr, uid, context)['departure_date'],
        'berths': lambda self, cr, uid, context: self._get_field_by_lead(cr, uid, context)['berths'],
    }
