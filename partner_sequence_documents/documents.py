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
from openerp.osv.orm import except_orm

class CustomPurchaseOrder(osv.osv):
    _inherit = 'purchase.order'

    def create(self, cr, uid, values, context = None):
        sequence_obj = self.pool.get('ir.sequence')
        if 'partner_id' in values:
            partner = self.pool.get('res.partner').browse(cr, uid, values['partner_id'])
            if partner.purchase_seq_id:
                values['name'] = self.pool.get('ir.sequence').next_by_id(cr, uid, partner.purchase_seq_id.id, context = context)
            else:
                if values.get('name', '/') == '/':
                    sequence_id = sequence_obj.search(cr, uid, [('code','=','purchase.order'),('is_custom','=',False)])
                    values['name'] =  sequence_id and sequence_obj.next_by_id(cr, uid, sequence_id[0], context = context) or '/'
        return super(CustomPurchaseOrder, self).create(cr, uid, values, context = context)

class CustomSaleOrder(osv.osv):
    _inherit = 'sale.order'

    def create(self, cr, uid, values, context = None):
        sequence_obj = self.pool.get('ir.sequence')
        if 'partner_id' in values:
            partner = self.pool.get('res.partner').browse(cr, uid, values['partner_id'])
            if partner.sale_seq_id:
                values['name'] = sequence_obj.next_by_id(cr, uid, partner.sale_seq_id.id, context = context)
            else:
                if values.get('name', '/') == '/':
                    sequence_id = sequence_obj.search(cr, uid, [('code','=','sale.order'),('is_custom','=',False)])
                    values['name'] =  sequence_id and sequence_obj.next_by_id(cr, uid, sequence_id[0], context = context) or '/'
        return super(CustomSaleOrder, self).create(cr, uid, values, context = context)
        
class CustomStockPicking(osv.osv):
    _inherit = 'stock.picking'

    def create(self, cr, uid, values, context = None):
        sequence_obj = self.pool.get('ir.sequence')
        if 'partner_id' in values:
            ptype_id = values.get('picking_type_id', context.get('default_picking_type_id', False))
            ptype = self.pool.get('stock.picking.type').browse(cr, uid, ptype_id, context=context)
            partner = self.pool.get('res.partner').browse(cr, uid, values['partner_id'])
            pick_seq = False
            if ptype.code == 'incoming':
                pick_seq = partner.picking_in_seq_id
            elif ptype.code == 'outgoing':
                pick_seq = partner.picking_out_seq_id
            if pick_seq:
                values['name'] = sequence_obj.next_by_id(cr, uid, pick_seq.id, context = context)
        return super(CustomStockPicking, self).create(cr, uid, values, context = context)

from openerp import models, api, fields
class CustomAccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, values):
        partner = self.env['res.partner'].browse(values['partner_id'])
        journal = self.env['account.journal'].browse(values['journal_id'])
        sequence_obj = self.pool.get('ir.sequence')
        number = ''
        inv_number = False
        if journal.type == 'sale':
            if partner.out_invoice_seq_id:
                inv_number = sequence_obj.next_by_id(self.env.cr, self.env.uid, partner.out_invoice_seq_id.id)
        if journal.type == 'sale_refund':
            if partner.out_refund_seq_id:
                inv_number = sequence_obj.next_by_id(self.env.cr, self.env.uid, partner.out_refund_seq_id.id)
        if journal.type == 'purchase':
            if partner.in_invoice_seq_id:
                number = sequence_obj.next_by_id(self.env.cr, self.env.uid, partner.in_invoice_seq_id.id)
        if journal.type == 'purchase_refund':
            if partner.in_refund_seq_id:
                number = sequence_obj.next_by_id(self.env.cr, self.env.uid, partner.in_refund_seq_id.id)
        values['reference'] = number
        if inv_number:
            values['invoice_number'] = inv_number
        return super(CustomAccountInvoice, self).create(values)


