# -*- encoding: utf-8 -*-
##############################################################################
#
#    POS Sale Report module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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

from openerp import models, fields
from openerp import tools
from openerp.tools.translate import _


class pos_sale_report(models.Model):
    _name = 'pos.sale.report'
    _description = 'POS orders and Sale orders aggregated report'
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    date = fields.Date(string='Order Date', readonly=True)
    product_id = fields.Many2one(
        'product.product', string='Product Variant', readonly=True)
    product_tmpl_id = fields.Many2one(
        'product.template', string='Product', readonly=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', readonly=True)
    category_id = fields.Many2one(
        'product.category', string='Category', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    location_id = fields.Many2one(
        'stock.location', string='Almacén', readonly=True)
    origin = fields.Char(string='Origin', readonly=True)
    qty = fields.Float(string='Quantity', readonly=True)
    amount = fields.Float(string='Total', readonly=True)

    # WARNING : this code doesn't handle uom conversion for the moment
    def _sale_order_select(self):
        select = """SELECT min(sol.id)*-1 AS id,
            so.date_order::date AS date,
            sol.product_id AS product_id,
            pp.product_tmpl_id AS product_tmpl_id,
            so.company_id AS company_id,
            so.partner_id AS partner_id,
            pt.categ_id AS category_id,
            '%s' AS origin,
            sum(sol.product_uom_qty) AS qty,
            so.warehouse_id AS location_id,
            so.amount_total AS amount
            FROM sale_order_line sol
            LEFT JOIN sale_order so ON so.id = sol.order_id
            LEFT JOIN product_product pp ON pp.id = sol.product_id
            left JOIN product_template pt ON pt.id = pp.product_tmpl_id
            LEFT JOIN product_category pc ON pc.id = pt.categ_id
            WHERE so.state NOT IN ('draft', 'sent', 'cancel')
            GROUP BY so.date_order, sol.product_id, pp.product_tmpl_id,
            so.company_id,so.partner_id,so.amount_total,pt.categ_id,so.warehouse_id
        """%(_("Sale Order"))
        return select

    def _pos_order_select(self):
        select = """SELECT min(pol.id) AS id,
            po.date_order::date AS date,
            pol.product_id AS product_id,
            pp.product_tmpl_id AS product_tmpl_id,
            po.company_id AS company_id,
            po.partner_id AS partner_id,
            pt.categ_id AS category_id,
            '%s' AS origin,
            sum(pol.qty) AS qty,
            po.location_id AS location_id,
            sum(pol.price_subtotal_incl) AS amount
            FROM pos_order_line pol
            LEFT JOIN pos_order po ON po.id = pol.order_id
            LEFT JOIN product_product pp ON pp.id = pol.product_id
            LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
            LEFT JOIN product_category pc ON pc.id = pt.categ_id
            WHERE po.state IN ('paid', 'done', 'invoiced')
            GROUP BY po.date_order, pol.product_id, pp.product_tmpl_id,
            po.company_id,partner_id,pt.categ_id,po.location_id
        """%(_("Point of Sale"))
        return select

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("CREATE OR REPLACE VIEW %s AS (%s UNION %s)" % (
            self._table, self._sale_order_select(), self._pos_order_select()))
