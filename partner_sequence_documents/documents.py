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
            if partner.custom_sequence:
                if not partner.purchase_seq_id:
                    raise except_orm('Advertencia','No está definida una secuencia de pedido de compras para este cliente')
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
            if partner.custom_sequence:
                if not partner.sale_seq_id:
                    raise except_orm('Advertencia','No está definida una secuencia de pedido de ventas para este cliente')
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
            partner = self.pool.get('res.partner').browse(cr, uid, values['partner_id'])
            if partner.custom_sequence:
                if not partner.picking_seq_id:
                    raise except_orm('Advertencia','No está definida una secuencia de albaranes para este cliente')
                values['name'] = sequence_obj.next_by_id(cr, uid, partner.picking_seq_id.id, context = context)
        return super(CustomStockPicking, self).create(cr, uid, values, context = context)

class CustomAccountMove(osv.osv):
    _inherit = "account.move"

    def post(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        invoice = context.get('invoice', False)
        valid_moves = self.validate(cr, uid, ids, context)

        if not valid_moves:
            raise osv.except_osv(_('Error!'), _('You cannot validate a non-balanced entry.\nMake sure you have configured payment terms properly.\nThe latest payment term line should be of the "Balance" type.'))
        obj_sequence = self.pool.get('ir.sequence')
        for move in self.browse(cr, uid, valid_moves, context=context):
            if move.name =='/':
                new_name = False
                journal = move.journal_id

                if invoice:
                    if invoice.partner_id.custom_sequence:
                        if invoice.type == 'out_invoice':
                            if not invoice.partner_id.out_invoice_seq_id:
                                raise except_orm('Advertencia','No está definida una secuencia de facturas de ventas para este cliente')
                            new_name = obj_sequence.next_by_id(cr, uid, invoice.partner_id.out_invoice_seq_id.id, context = context)
                        elif invoice.type == 'out_refund':
                            if not invoice.partner_id.out_refund_seq_id:
                                raise except_orm('Advertencia','No está definida una secuencia de facturas rectificativas de ventas para este cliente')
                            new_name = obj_sequence.next_by_id(cr, uid, invoice.partner_id.out_refund_seq_id.id, context = context)
                        else:
                            new_name = invoice.internal_number and invoice.internal_number or '/'
                    else:
                        if journal.sequence_id:
                            c = {'fiscalyear_id': move.period_id.fiscalyear_id.id}
                            new_name = obj_sequence.next_by_id(cr, uid, journal.sequence_id.id, c)
                        else:
                            raise osv.except_osv(_('Error!'), _('Please define a sequence on the journal.'))
                else:
                    if journal.sequence_id:
                        c = {'fiscalyear_id': move.period_id.fiscalyear_id.id}
                        new_name = obj_sequence.next_by_id(cr, uid, journal.sequence_id.id, c)
                    else:
                        raise osv.except_osv(_('Error!'), _('Please define a sequence on the journal.'))

                if new_name:
                    self.write(cr, uid, [move.id], {'name':new_name})

        cr.execute('UPDATE account_move '\
                   'SET state=%s '\
                   'WHERE id IN %s',
                   ('posted', tuple(valid_moves),))
        self.invalidate_cache(cr, uid, context=context)
        return True


from openerp import models, api, fields
class CustomAccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, values):
        partner = self.env['res.partner'].browse(values['partner_id'])
        journal = self.env['account.journal'].browse(values['journal_id'])
        sequence_obj = self.pool.get('ir.sequence')
        if partner.custom_sequence:
            number = '/'
            if journal.type == 'purchase':
                if not partner.in_invoice_seq_id:
                    raise except_orm('Advertencia','No está definida una secuencia de facturas de compras para este cliente')
                number = sequence_obj.next_by_id(self.env.cr, self.env.uid, partner.in_invoice_seq_id.id)
            elif journal.type == 'purchase_refund':
                if not partner.in_refund_seq_id:
                    raise except_orm('Advertencia','No está definida una secuencia de facturas rectificativas de compras para este cliente')
                number = sequence_obj.next_by_id(self.env.cr, self.env.uid, partner.in_refund_seq_id.id)
            values['reference'] = number
        return super(CustomAccountInvoice, self).create(values)


