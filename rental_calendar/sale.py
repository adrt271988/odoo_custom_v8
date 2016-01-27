# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.osv import osv, fields
import datetime

class rental_calendar_sale_order(osv.osv):
    _inherit = "sale.order"

    def _get_global_end_date(self, cr, uid, ids, name, arg, context=None):
        res = {}
        dates_list = []
        for sale in self.browse(cr, uid, ids, context=context):
            dates_list = []
            for line in sale.order_line:
                if line.end_date:
                    dates_list.append(line.end_date)
            res[sale.id] = dates_list and max(dates_list) or False
        return res

    _columns={
                'global_end_date': fields.function(_get_global_end_date, store=True,
                                    type='date', string='Fecha Límite Global',
                                    help="La mayor fecha final entre las líneas del pedido"),
    }
    
