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
            'partner_id': fields.many2one('res.partner','Cliente',help="Seleccione el cliente a facturar"),
            'wizard_line': fields.one2many('rental.invoicemissing.line','wizard_id','Alquileres no Retornados'),
        }

    def onchange_partner(self, cr, uid, ids, partner_id, context=None):
        if context is None:
            context = {}
        rental_o2m = []
        lines = []
        if partner_id:
            rental_obj = self.pool.get('sale.rental')
            rental_ids = rental_obj.search(cr, uid, [('non_rel_partner_id','=',partner_id)])
            if rental_ids:
                for rental in rental_obj.browse(cr, uid, rental_ids):
                    if rental.state == "out" and rental.in_state not in ["cancel","done"]:
                        rental_o2m.append(rental)
            # Tenemos los alquileres a mostrar en el wizard segun el cliente
            # Realizamos las líneas
            for r in rental_o2m:
                vals = {
                            'rental_id': r.id,
                            'product_id': r.rented_product_id.id,
                            'sale_id': r.start_order_id.id,
                            'qty': r.rental_qty,
                            'state': r.state,
                            'in_state': r.in_state,
                            'out_state': r.out_state,
                            'end_date': r.end_date,
                }
                lines.append((0,0,vals))
                
        return {'value': {'wizard_line': lines}}

    def _create_rental_missing_invoice(self, cr, uid, order, invoice_lines, origin, context=None):
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
            'origin': origin,
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
            'section_id' : order.section_id.id,
            'comment': "Facturados productos no regresados por pedidos %s"%origin,
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
        wizard = self.browse(cr, uid, ids[0], context=context)
        inv_lines = []
        moves = []
        sales = []
        for line in wizard.wizard_line:
            invLine_vals = self._prepare_rental_missing_invoice_line(cr, uid, line.rental_id.start_order_line_id, context = context)
            inv_lines.append((0,0,invLine_vals))
            moves.append(line.rental_id.in_move_id.id)
            if line.sale_id.name not in sales:
                sales.append(line.sale_id.name)
        if inv_lines:
            origin = ', '.join(sales)
            invoice_id = self._create_rental_missing_invoice(cr, uid, line.sale_id, inv_lines, origin, context = context)
            if invoice_id:
                self.pool.get('stock.move').action_cancel(cr, uid, moves, context)

        return {'type': 'ir.actions.act_window_close'}

    _defaults= {
                'description': "Genere las facturas de los productos seleccionados"
    }

class rental_invoicemissing_line(osv.osv_memory):
    _name = "rental.invoicemissing.line"

    _columns = {
            'wizard_id': fields.many2one('rental.invoice.missing','Wizard'),
            'rental_id': fields.many2one('sale.rental','Alquiler'),
            'product_id': fields.many2one('product.product','Producto'),
            'sale_id': fields.many2one('sale.order','Pedido'),
            'qty': fields.integer('Cantidad alquilada'),
            'state': fields.selection([
                                        ('ordered', 'En Pedido'),
                                        ('out', 'Alquilado'),
                                        ('sell_progress', 'Venta en Progreso'),
                                        ('sold', 'Vendido'),
                                        ('in', 'Regresado'),
                                        ], 'Estatus'),
            'in_state': fields.selection([('draft', 'Nuevo'),
                                   ('cancel', 'Cancelado'),
                                   ('waiting', 'Esperando movimiento'),
                                   ('confirmed', 'Esperando disponibilidad'),
                                   ('assigned', 'Disponible'),
                                   ('done', 'Realizado'),
                                   ], 'Retorno'),
            'out_state': fields.selection([('draft', 'Nuevo'),
                                   ('cancel', 'Cancelado'),
                                   ('waiting', 'Esperando movimiento'),
                                   ('confirmed', 'Esperando disponibilidad'),
                                   ('assigned', 'Disponible'),
                                   ('done', 'Realizado'),
                                   ], 'Salida'),
            'end_date': fields.date('Fecha fin'),
    }
