# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    $Id: account.py 1005 2005-07-25 08:41:42Z nicoe $
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
from datetime import datetime, date, time, timedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _

import base64
from openerp.addons.web import http
#~ from openerp.exceptions import except_orm, Warning
#~ import openerp.addons.web.http as oeweb
#~ from openerp import models, fields, api, _
#~ from operator import attrgetter
try:
    import xlwt
except ImportError:
    xlwt = None
import re
from cStringIO import StringIO

class wizard_receipt_txt(osv.osv_memory):
    _name = 'wizard.receipt.txt'
    _description = 'Wizard that generate txt.'
    _columns = {

        'session_id': fields.many2one('pos.session', 'Sesión'),
        'session_ids': fields.many2many('pos.session', 'receipt_sessions_rel','wizard_id','session_id','Sesiones'),
        'filter_session': fields.selection([('single', 'Sesión'),
                                            ('multi', 'Multiples sesiones'),
                                            ('all', 'Todas las sesiones')],
                                            string='Filtro de Sesiones', select=True, required=True),
        'filter_date': fields.selection([('daily', 'Por dia'),
                                         ('range', 'Rango de fechas'),],
                                         string='Filtro de Fechas'),

        'date': fields.date('Fecha', required=True),
        'date_from': fields.date('Desde', required=True),
        'date_to': fields.date('Hasta', required=True),
    }

    _defaults = {
        'date': fields.datetime.now,
        'date_from': fields.datetime.now,
        'date_to': fields.datetime.now,
    }

    def generate_txt(self, cr, uid, ids, context= None):
        if context is None:
            context = {}
        wzd_values = self.read(cr,uid,ids,context=context)[0]
        pos_order_obj = self.pool.get('pos.order')
        filter_session = wzd_values['filter_session']
        filter_date = wzd_values.get('filter_date',False)
        pos_order_ids = []
        if filter_session == 'all':
            if filter_date:
                pos_order_ids = filter_date == 'daily' and pos_order_obj.search(cr, uid, [('date_order','=',wzd_values['date'])]) \
                    or pos_order_obj.search(cr, uid, ['|',('date_order','>=',wzd_values['date_from']),('date_order','<=',wzd_values['date_to'])])
            else:
                pos_order_ids = pos_order_obj.search(cr, uid, [])
        elif filter_session == 'multi':
            session_ids = wzd_values.get('session_ids') and wzd_values['session_ids'] or []
            if session_ids:
                for session in self.pool.get('pos.session').browse(cr, uid, session_ids):
                    pos_order_ids+=[order.id for order in session.order_ids]
        else:
            session_id = wzd_values.get('session_id') and wzd_values['session_id'][0] or False
            pos_order_ids = session_id and pos_order_obj.search(cr, uid, [('session_id','=',session_id)]) or []

        path = '/tmp/pos_%s.txt'% (datetime.today())
        txtFile = open(path,'w')
        for order in pos_order_obj.browse(cr, uid, pos_order_ids, context=context):
            date = datetime.strptime(order.date_order, '%Y-%m-%d')
            txtFile.write("\n\n")
            company = '           %s'%order.company_id.name
            partner = '         %s'%order.partner_id and order.partner_id.name or 'N/A'
            user = '       Usuario: %s'%order.user_id.name
            date = '          Fecha: %s'%date.strftime("%d-%m-%Y")
            ref = '       %s'%order.pos_reference
            txtFile.write("%s\n%s\n%s\n%s\n%s\n"%(company,partner,user,date,ref))
            txtFile.write("\n   Descripción     Cantidad  Precio\n")
            for line in order.lines:
                str_length = len(line.product_id.name)
                str_res = 15 - str_length
                product = str_length > 15 and line.product_id.name[0:15] or \
                            line.product_id.name+'{s:{c}{n}}'.format(s="",n=str_res,c='')
                txtFile.write("   %s     %s    %s\n"%(product,line.qty,line.price_subtotal))
            txtFile.write("\n\n                   Impuestos: %s"%order.amount_tax)
            txtFile.write("\n                   Total:    %s"%order.amount_total)
            txtFile.write("\n")
            txtFile.write("\n   Método de Pago         Importe\n")
            for payment in order.statement_ids:
                txtFile.write("   %s          %s\n"%(payment.journal_id.name[0:15],payment.amount))
            txtFile.write("\n\n------------------------------------------\n")

        txtFile.close()
        arch = open(path, 'r').read()
        data = base64.encodestring(arch)
        attach_vals = {
                 'name':'File#%s_%s.txt' % (ids[0],datetime.today().strftime("%d-%m-%Y")),
                 'datas':data,
                 'datas_fname':'File#%s_%s.txt' % (ids[0],datetime.today().strftime("%d-%m-%Y")),
                 }
        doc_id = self.pool.get('ir.attachment').create(cr, uid, attach_vals)
        return {
                    'type' : 'ir.actions.act_url',
                    'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=name&id=%s' % (doc_id),
                    'target': 'self',
                    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
