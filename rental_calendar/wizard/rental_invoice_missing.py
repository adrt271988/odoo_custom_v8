# -*- encoding: utf-8 -*-
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import unicodedata
import logging
import openerp.netsvc as netsvc
import time
from datetime import datetime, timedelta
from  dateutil.relativedelta import relativedelta


class rental_invoice_missing(osv.osv_memory):
    _name = "rental.invoice.missing"

    _columns = {
            'partner_id': fields.many2one('res.partner','Cliente'),
        }

    def generate_missing_invoice(self,cr,uid,ids,context=None):
        if context is None:
            context = {}

        print ids
        wizard = ids and self.browse(cr, uid, ids[0], context=context) or False
        rental = self.pool.get('sale.rental')
        print '*******',wizard.partner_id.id
        rental_ids = rental.search(cr, uid, [('partner_id','=',wizard.partner_id.id)])
        if rental_ids:
            for rent in rental.browse(cr, uid, rental_ids):
                if rent.state == 'out':
                    print 'something'
        else:
            raise osv.except_osv(_('Error'), _('No existen alquileres a nombre de este cliente!'))

        return {'type': 'ir.actions.act_window_close'}
