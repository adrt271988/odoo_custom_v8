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

from openerp.osv import fields,osv

class pos_order_filter_res_partner(osv.osv):
    _inherit = 'res.partner'

    def _pos_order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
        for partner in self.browse(cr, uid, ids, context):
            res[partner.id] = len(partner.pos_order_ids) + len(partner.mapped('child_ids.pos_order_ids'))
        return res

    _columns = {
        'pos_order_count': fields.function(_pos_order_count, string='# of PdV Pedidos', type='integer'),
        'pos_order_ids': fields.one2many('pos.order','partner_id','PdV Pedidos')
    }

