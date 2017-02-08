# -*- encoding: utf-8 -*-
##############################################################################
#
#    Custom module for Odoo
#    @author Alexander Rodriguez <adrt271988@gmail.com>
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
from openerp.osv import fields,osv

class CustomResPartner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'custom_sequence': fields.boolean('Utiliza secuencias personalizadas',help="Si habilita esta opción permitirá asociar las secuencias de los documentos en este cliente"),
        'purchase_seq_id': fields.many2one('ir.sequence','Secuencia Pedidos de Compra', help="Secuencia personalizada para pedidos de compra"),
        'sale_seq_id': fields.many2one('ir.sequence','Secuencia Pedidos de Venta', help="Secuencia personalizada para pedidos de venta"),
        'in_invoice_seq_id': fields.many2one('ir.sequence','Secuencia Facturas de Compra', help="Secuencia personalizada para facturas de compra"),
        'out_invoice_seq_id': fields.many2one('ir.sequence','Secuencia Facturas de Venta', help="Secuencia personalizada para facturas de venta"),
        'picking_seq_id': fields.many2one('ir.sequence','Secuencia Albaránes', help="Secuencia personalizada para albaránes"),
        'in_refund_seq_id': fields.many2one('ir.sequence','Secuencia Notas de Crédito Compras', help="Secuencia personalizada para notas de crédito de compra"),
        'out_refund_seq_id': fields.many2one('ir.sequence','Secuencia Notas de Crédito de Ventas', help="Secuencia personalizada para notas de crédito de venta"),
    }
