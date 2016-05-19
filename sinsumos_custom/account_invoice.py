# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from number_to_letter import number_to_letter
from openerp.osv import osv, fields
import datetime

class sinsumos_account_invoice(osv.osv):
    _inherit = "account.invoice"

    def _get_items(self, cr, uid, ids, field_name, arg, context=None):
        context = context or {}
        res = {}.fromkeys(ids, 0)
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = len(map(lambda x: x.id, invoice.invoice_line))
        return res

    def _number_to_string(self, cr, uid, ids, field_name, arg, context=None):
        context = context or {}
        res = {}.fromkeys(ids, 0)
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = number_to_letter.to_word(invoice.amount_total, mi_moneda = 'VEF')
        return res

    def _get_picking(self, cr, uid, ids, field_name, arg, context=None):
        context = context or {}
        res = {}.fromkeys(ids, 0)
        for invoice in self.browse(cr, uid, ids, context=context):
            if invoice.origin:
                picking = self.pool.get('stock.picking')
                picking_id = picking.search(cr, uid, [('origin','=',invoice.origin)])
                if picking_id:
                    res[invoice.id] = picking_id[0]
        return res

    _columns = {
                'items': fields.function(_get_items, type='integer',
                        string="Items",store=True),
                'amount_total_string': fields.function(_number_to_string, type='char',
                        string="Amount Total String",store=False),
                'picking_id': fields.function(_get_picking, type='many2one', relation='stock.picking', string='Albarán',
                            store=True, readonly=True),
    }
