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
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _

class wizard_receipt_txt(osv.osv_memory):
    _name = 'wizard.receipt.txt'
    _description = 'Wizard that generate txt.'
    _columns = {

        'session_id': fields.many2one('pos.session', 'Sesión'),
        'session_ids': fields.many2many('pos.session', 'receipt_sessions_rel','wizard_id','session_id','Sesiones'),
        'filter_session': fields.selection([('single', 'Sesión'),
                                            ('multi', 'Multiples sesiones'),
                                            ('all', 'Todas las sesiones')],
                                            string='Selección', required=True),
        'filter_date': fields.selection([('daily', 'Por dia'),
                                         ('range', 'Rango de fechas'),],
                                         string='Selección', required=True),

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
        values = self.read(cr,uid,ids,context=context)[0]
        print values
        return True

    def action_txt(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        values = self.read(cr,uid,ids, context=context)
        period_id = values[0]['period_id'][0]
        periodo = values[0]['period_id'][1].replace('/','-')
        move_line_obj = self.pool.get('account.move.line')
        #archivo = open('/mnt/gsist06/OpenERP/txt/salida/'+periodo+'.txt','w')
        ruta = '/home/openerp/txt-activos/'+periodo+'.txt'
        archivo = open(ruta,'w')

        query = cr.execute(''' SELECT ac.code, ac.name as cuenta, line.name, line.credit as credito, line.debit as debito
                                FROM account_move_line as line
                                JOIN account_account ac on ac.id = line.account_id
                                JOIN account_journal jo on jo.id = line.journal_id
                                WHERE line.period_id = %s and jo.code = 'DADA' ORDER BY line.name'''%period_id)
        query = cr.dictfetchall()

        for line in query:
            cuenta = str(line['code']).zfill(11)
            descrip =  len(line['name']) > 25 and  line['name'][0:25] or line['name'].ljust(25,'-')

            if line['debito'] > 0.00:
                tipo = '1'
                monto = str(int(line['debito']*100)).zfill(10)
                archivo.write("%s\n"%(cuenta+tipo+descrip+monto))
            else:
                tipo = '2'
                monto= str(int(line['credito']*100)).zfill(10)
                archivo.write("%s\n"%(cuenta+tipo+descrip+monto))

        archivo.close()
        return {
                'type': 'ir.actions.act_window',
                'name': 'confirm.xml',
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'confirm',
                'target': 'new',
                'context': context,
                }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
