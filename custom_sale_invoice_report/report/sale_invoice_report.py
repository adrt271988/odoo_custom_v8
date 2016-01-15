# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import tools
import openerp.addons.decimal_precision as dp
from openerp.osv import fields,osv

class sale_invoice_report(osv.osv):
    _name = "sale.invoice.report"
    _description = "ARA de Ventas"
    _auto = False
    _rec_name = 'date'

    def _compute_amounts_in_user_currency(self, cr, uid, ids, field_names, args, context=None):
        """Compute the amounts in the currency of the user
        """
        if context is None:
            context={}
        currency_obj = self.pool.get('res.currency')
        currency_rate_obj = self.pool.get('res.currency.rate')
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        user_currency_id = user.company_id.currency_id.id
        currency_rate_id = currency_rate_obj.search(
            cr, uid, [
                ('rate', '=', 1),
                '|',
                    ('currency_id.company_id', '=', user.company_id.id),
                    ('currency_id.company_id', '=', False)
                ], limit=1, context=context)[0]
        base_currency_id = currency_rate_obj.browse(cr, uid, currency_rate_id, context=context).currency_id.id
        res = {}
        ctx = context.copy()
        for item in self.browse(cr, uid, ids, context=context):
            ctx['date'] = item.date
            price_total = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.price_total, context=ctx)
            price_average = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.price_average, context=ctx)
            residual = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.residual, context=ctx)
            res[item.id] = {
                'user_currency_price_total': price_total,
                'user_currency_price_average': price_average,
                'user_currency_residual': residual,
            }
        return res

    _columns = {
        'date': fields.date('Fecha', readonly=True),
        'product_id': fields.many2one('product.product', 'Producto', readonly=True),
        'product_qty':fields.float('Cantidad de Productos', readonly=True),
        'uom_name': fields.char('Unidad de Medida Refrencia', size=128, readonly=True),
        'payment_term': fields.many2one('account.payment.term', 'Condición de Pago', readonly=True),
        'period_id': fields.many2one('account.period', 'Período', domain=[('state','<>','done')], readonly=True),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Posición Fiscal', readonly=True),
        'currency_id': fields.many2one('res.currency', 'Moneda', readonly=True),
        'categ_id': fields.many2one('product.category','Categoría de Productos', readonly=True),
        'categ_parent': fields.many2one('product.category','Categoría Padre', readonly=True),
        'journal_id': fields.many2one('account.journal', 'Diario', readonly=True),
        #~ 'partner_id': fields.many2one('res.partner', 'Empresa', domain=[('customer','=','True'),('supplier','=','False')], readonly=True),
        'partner_id': fields.many2one('res.partner', 'Empresa', readonly=True),
        'commercial_partner_id': fields.many2one('res.partner', 'Compañía de la empresa', help="Commercial Entity"),
        'company_id': fields.many2one('res.company', 'Compañía', readonly=True),
        'user_id': fields.many2one('res.users', 'Comercial', readonly=True),
        'price_total': fields.float('Total sin Impuesto', readonly=True),
        'user_currency_price_total': fields.function(_compute_amounts_in_user_currency, string="Total sin Impuesto", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
        'price_average': fields.float('Costo Promedio', readonly=True, group_operator="avg"),
        'user_currency_price_average': fields.function(_compute_amounts_in_user_currency, string="Costo Promedio", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
        'currency_rate': fields.float('Tasa de Conversión', readonly=True),
        'nbr': fields.integer('# Facturas', readonly=True),  # TDE FIXME master: rename into nbr_lines
        'type': fields.selection([
            ('out_invoice','Factura de Cliente'),
            ('in_invoice','Factura de Proveedor'),
            ('out_refund','Devolución a Cliente'),
            ('in_refund','Devolución a Proveedor'),
            ],'Tipo de Factura', readonly=True),
        'state': fields.selection([
            ('draft','Borrador'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Abierto'),
            ('paid','Cerrado'),
            ('cancel','Cancelado')
            ], 'Estado Factura', readonly=True),
        'date_due': fields.date('Fecha de Vencimiento', readonly=True),
        'account_id': fields.many2one('account.account', 'Cuenta Contable',readonly=True),
        'account_line_id': fields.many2one('account.account', 'Línea de Cuenta Contable',readonly=True),
        'partner_bank_id': fields.many2one('res.partner.bank', 'Cuenta Bancaria',readonly=True),
        'residual': fields.float('Saldo Pendiente', readonly=True),
        'user_currency_residual': fields.function(_compute_amounts_in_user_currency, string="Saldo Pendiente", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
        'country_id': fields.many2one('res.country', 'País'),
        'section_id': fields.many2one('crm.case.section', 'Equipos de Ventas'),
    }
    _order = 'date desc'

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total', 'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position',
            'journal_id', 'partner_bank_id', 'partner_id', 'payment_term',
            'period_id', 'residual', 'state', 'type', 'user_id',
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uos_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.category': ['parent_id'],
        'product.template': ['categ_id'],
        'product.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    def _select(self):
        select_str = """
            SELECT sub.id, sub.date, sub.product_id, sub.partner_id, sub.country_id,
                sub.payment_term, sub.period_id, sub.uom_name, sub.currency_id, sub.journal_id,
                sub.fiscal_position, sub.user_id, sub.company_id, sub.nbr, sub.type, sub.state, sub.section_id,
                sub.categ_id, sub.categ_parent, sub.date_due, sub.account_id, sub.account_line_id, sub.partner_bank_id,
                sub.product_qty, sub.price_total as price_total, sub.price_average /cr.rate as price_average,
                cr.rate as currency_rate, sub.residual / cr.rate as residual, sub.commercial_partner_id as commercial_partner_id
        """
        return select_str

    def _sub_select(self):
        select_str = """
                SELECT min(ail.id) AS id,
                    ai.date_invoice AS date,
                    ail.product_id, ai.partner_id, ai.payment_term, ai.period_id,
                    u2.name AS uom_name,
                    ai.currency_id, ai.journal_id, ai.fiscal_position, ai.user_id, ai.company_id,
                    count(ail.*) AS nbr,
                    ai.type, ai.state, pt.categ_id, ai.date_due, ai.account_id, ail.account_id AS account_line_id,
                    ai.partner_bank_id,
                    SUM(CASE
                         WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN (- ail.quantity) / u.factor * u2.factor
                            ELSE ail.quantity / u.factor * u2.factor
                        END) AS product_qty,
                    SUM(CASE
                         WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                            THEN - ail.price_subtotal
                            ELSE ail.price_subtotal
                        END) AS price_total,
                    CASE
                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN SUM(- ail.price_subtotal)
                        ELSE SUM(ail.price_subtotal)
                    END / CASE
                           WHEN SUM(ail.quantity / u.factor * u2.factor) <> 0::numeric
                               THEN CASE
                                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                                        THEN SUM((- ail.quantity) / u.factor * u2.factor)
                                        ELSE SUM(ail.quantity / u.factor * u2.factor)
                                    END
                               ELSE 1::numeric
                          END AS price_average,
                    CASE
                     WHEN ai.type::text = ANY (ARRAY['out_refund'::character varying::text, 'in_invoice'::character varying::text])
                        THEN - ai.residual
                        ELSE ai.residual
                    END / (SELECT count(*) FROM account_invoice_line l where invoice_id = ai.id) *
                    count(*) AS residual,
                    ai.commercial_partner_id as commercial_partner_id,
                    partner.country_id,
                    pc.parent_id as categ_parent,
                    ai.section_id as section_id
        """
        return select_str

    def _from(self):
        from_str = """
                FROM account_invoice_line ail
                JOIN account_invoice ai ON ai.id = ail.invoice_id
                JOIN res_partner partner ON ai.commercial_partner_id = partner.id
                LEFT JOIN product_product pr ON pr.id = ail.product_id
                left JOIN product_template pt ON pt.id = pr.product_tmpl_id
                left JOIN product_category pc ON pc.id = pt.categ_id
                LEFT JOIN product_uom u ON u.id = ail.uos_id
                LEFT JOIN product_uom u2 ON u2.id = pt.uom_id
                WHERE ai.state != 'cancel'
        """
        return from_str

    def _group_by(self):
        group_by_str = """
                GROUP BY ail.product_id, ai.date_invoice, ai.id,
                    ai.partner_id, ai.payment_term, ai.period_id, u2.name, u2.id, ai.currency_id, ai.journal_id,
                    ai.fiscal_position, ai.user_id, ai.company_id, ai.type, ai.state, pt.categ_id,
                    ai.date_due, ai.account_id, ail.account_id, ai.partner_bank_id, ai.residual,
                    ai.amount_total, ai.commercial_partner_id, partner.country_id, pc.parent_id, ai.section_id
        """
        return group_by_str

    def init(self, cr):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            WITH currency_rate (currency_id, rate, date_start, date_end) AS (
                SELECT r.currency_id, r.rate, r.name AS date_start,
                    (SELECT name FROM res_currency_rate r2
                     WHERE r2.name > r.name AND
                           r2.currency_id = r.currency_id
                     ORDER BY r2.name ASC
                     LIMIT 1) AS date_end
                FROM res_currency_rate r
            )
            %s
            FROM (
                %s %s %s
            ) AS sub
            JOIN currency_rate cr ON
                (cr.currency_id = sub.currency_id AND
                 cr.date_start <= COALESCE(sub.date, NOW()) AND
                 (cr.date_end IS NULL OR cr.date_end > COALESCE(sub.date, NOW())))
        )""" % (
                    self._table,
                    self._select(), self._sub_select(), self._from(), self._group_by()))


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
