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

    def _prepare_rental_missing_invoice_line(self, cr, uid, line, context=None):
        """Prepare the dict of values to create the new invoice line for a
           sales order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: sale.order.line record to invoice
           :return: dict of values to create() the invoice line
        """
        res = {}
        product_id = line.product_id.rented_product_id
        account_id = product_id.property_account_income.id
        if not account_id:
            account_id = product_id.categ_id.property_account_income_categ.id
        if not account_id:
            raise osv.except_osv(_('Error!'),
                    _('Please define income account for this product: "%s" (id:%d).') % \
                        (product_id.name, product_id.id,))
        uosqty = line.rental_qty
        uos_id = product_id.uom_id.id
        pu = 0.0
        if uosqty:
            pu = round(product_id.list_price * uosqty, self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Price'))
        fpos = line.order_id.fiscal_position or False
        account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, account_id)
        if not account_id:
            raise osv.except_osv(_('Error!'),
                        _('There is no Fiscal Position defined or Income category account defined for default properties of Product categories.'))
        res = {
            'name': line.name,
            'sequence': line.sequence,
            'origin': line.order_id.name,
            'account_id': account_id,
            'price_unit': pu,
            'quantity': uosqty,
            'discount': line.discount,
            'uos_id': uos_id,
            'product_id': product_id.id,
            'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
            'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
        }

        return res
    
    def generate_missing_invoice(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        rental_ids = context.get("active_ids",False)
        if rental_ids:
            sale_obj = self.pool.get('sale.order')
            rental_obj = self.pool.get('sale.rental')
            sale_line_obj = self.pool.get('sale.order.line')
            for rental in rental_obj.browse(cr,uid,rental_ids):
                if rental.state == "out":
                    print '***************',sale_line_obj._prepare_rental_missing_invoice_line(cr, uid, rental.start_order_line_id, context = context)
        else:
            raise osv.except_osv(_('Error'), _('Seleccione al menos un registro!'))

        return {'type': 'ir.actions.act_window_close'}

    _defaults= {
                    'description': "Genere las facturas de los productos seleccionados"
    }
