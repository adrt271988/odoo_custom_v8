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

import openerp
from openerp.addons.crm import crm
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
from openerp.tools import html2plaintext


class inherit_custom_account_invoice(osv.osv):
    """ Inherit Account Invoice """

    _inherit = 'account.invoice'

    def default_get(self, cr, uid, fields_list, context=None):
        context = context and context or {}
        res = super(inherit_custom_account_invoice, self).default_get(cr, uid, fields_list, context)
        partner_id = context.get('partner_id')
        name = context.get('name')
        res.update({'partner_id':partner_id and partner_id or '', 'name':name and name or ''})
        return res
        
class inherit_crm_helpdesk(osv.osv):
    """ Inherit HelpDesk """

    _inherit = 'crm.helpdesk'

    def create_invoice(self, cr, uid, ids, context=None):
        context = context and context or {}
        helpdesk = self.browse(cr, uid, ids[0], context)
        context.update({
                            'partner_id': helpdesk.partner_id.id,
                            'name': helpdesk.name,
                        })
        view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account', 'invoice_form')
        return {
		    'view_mode': 'form',
		    'view_id': view_id[1],
		    'view_type': 'form',
		    'res_model': 'account.invoice',
		    'type': 'ir.actions.act_window',
		    'target': 'new',
		    'context': context,
            'nodestroy': True,
		}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
