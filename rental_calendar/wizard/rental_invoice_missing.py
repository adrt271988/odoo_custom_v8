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
            'description': fields.char('Descripción'),
        }

    def generate_missing_invoice(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        rental_ids = context.get("active_ids",False)
        if rental_ids:
            sale_obj = self.pool.get('sale.order')
            rental_obj = self.pool.get('sale.rental')
            for rental in rental_obj.browse(cr,uid,rental_ids):
                print "something"
        else:
            raise osv.except_osv(_('Error'), _('Seleccione al menos un registro!'))

        return {'type': 'ir.actions.act_window_close'}

    _defaults= {
                    'description': "Genere las facturas de los productos seleccionados"
    }
