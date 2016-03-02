# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.tools import number_to_letter
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

    _columns = {
                'items': fields.function(_get_items, type='integer',
                        string="Items",store=True),
                'amount_total_string': fields.function(_number_to_string, type='char',
                        string="Amount Total String",store=False),
    }
