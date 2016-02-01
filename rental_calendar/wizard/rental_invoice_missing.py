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

    def get_order_by_rental(self, cr, uid, rental_ids, rental_brw, context = None):
        sales = []
        for rental in rental_brw:
            if rental.state == "out" and rental.in_state != "cancel":
                sale_id = rental.start_order_id
                if sale_id not in sales:
                    sales.append(sale_id)
        return sales

    def _create_rental_missing_invoice(self, cr, uid, order, invoice_lines, context=None):
        """Prepare the dict of values to create the new invoice for a
           sales order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: sale.order record to invoice
           :param list(dict) line: list of dictionaries of invoice lines values that must be
                                  attached to the invoice
           :return: create_id
        """
        if context is None:
            context = {}
        invoice_obj = self.pool.get('account.invoice')
        journal_ids = self.pool.get('account.journal').search(cr, uid,
            [('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
            limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                _('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
        invoice_vals = {
            'name': order.client_order_ref or '',
            'origin': order.name,
            'type': 'out_invoice',
            'reference': order.client_order_ref or order.name,
            'account_id': order.partner_invoice_id.property_account_receivable.id,
            'partner_id': order.partner_invoice_id.id,
            'journal_id': journal_ids[0],
            'invoice_line': invoice_lines,
            'currency_id': order.pricelist_id.currency_id.id,
            'comment': order.note,
            'payment_term': order.payment_term and order.payment_term.id or False,
            'fiscal_position': order.fiscal_position.id or order.partner_invoice_id.property_account_position.id,
            'date_invoice': context.get('date_invoice', False),
            'company_id': order.company_id.id,
            'user_id': order.user_id and order.user_id.id or False,
            'section_id' : order.section_id.id
        }
        return invoice_obj.create(cr, uid, invoice_vals, context=context)

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
            pu = round(product_id.list_price, self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Price'))
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
            rental_obj = self.pool.get('sale.rental')
            rental_brw = rental_obj.browse(cr,uid,rental_ids)
            sales = self.get_order_by_rental(cr, uid, rental_ids, rental_brw, context = context)
            if sales:
                for sale in sales:
                    inv_lines = []
                    moves = []
                    for rental in rental_brw:
                        if rental.state == "out" and rental.in_state != "cancel":
                            inv_line_vals = self._prepare_rental_missing_invoice_line(cr, uid, rental.start_order_line_id, context = context)
                            inv_lines.append((0,0,inv_line_vals))
                            moves.append(rental.in_move_id.id)
                    if inv_lines:
                        invoice_id = self._create_rental_missing_invoice(cr, uid, sale, inv_lines, context = context)
                        if invoice_id:
                            self.pool.get('stock.move').action_cancel(cr, uid, moves, context)
        else:
            raise osv.except_osv(_('Error'), _('Seleccione al menos un registro!'))

        return {'type': 'ir.actions.act_window_close'}

    _defaults= {
                    'description': "Genere las facturas de los productos seleccionados"
    }
