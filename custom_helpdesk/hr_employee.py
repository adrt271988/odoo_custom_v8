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


class inherit_custom_hr_employee(osv.osv):
    """ Inherit Hr Employee """

    _inherit = 'hr.employee'

    def prepare_payment(self, cr, uid, ids, context=None):
        context = context and context or {}
        employee = self.browse(cr, uid, ids[0], context)
        done_tickets = [];
        for hd_ticket in employee.crm_helpdesk_ids:
            if hd_ticket.state == "done":
                done_tickets.append(hd_ticket.id)
        if not done_tickets:
            raise osv.except_osv(_('Error!'), _('There is no Support Tickets in Done state!'))
        context.update({
                            'partner_id': employee.user_id.partner_id.id,
                        })
        view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_voucher', 'view_vendor_payment_form')
        return {
		    'view_mode': 'form',
		    'view_id': view_id[1],
		    'view_type': 'form',
		    'res_model': 'account.voucher',
		    'type': 'ir.actions.act_window',
		    'target': 'new',
		    'context': context,
            'nodestroy': True,
		}

    _columns = {
            'crm_helpdesk_ids': fields.one2many('crm.helpdesk','user_id','Helpdesk Tickets'),
            }
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
