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

class CustomIrSequence(osv.osv):
    _inherit = 'ir.sequence'

    def _is_custom(self, cr, user, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids)
        partner_obj = self.pool.get('res.partner')
        for sequence in self.browse(cr, user, ids, context=context):
            partner_ids = partner_obj.search(cr, user, ['|','|','|','|','|','|',
                                                        ('purchase_seq_id','=',sequence.id),
                                                        ('sale_seq_id','=',sequence.id),
                                                        ('picking_in_seq_id','=',sequence.id),
                                                        ('picking_out_seq_id','=',sequence.id),
                                                        ('in_invoice_seq_id','=',sequence.id),
                                                        ('out_invoice_seq_id','=',sequence.id),
                                                        ('out_refund_seq_id','=',sequence.id),
                                                        ('in_refund_seq_id','=',sequence.id),
                                                    ])
            if partner_ids:
                res[sequence.id] = True
        return res

    _columns = {
        'is_custom': fields.function(_is_custom,type="boolean",string='Es persoanlizada',help="Indica si la secuencia está asociada a algún partner (Cliente o Proveedor)",store=True),
    }
