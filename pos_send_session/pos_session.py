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

class pos_session_inherit(osv.osv):
    _inherit = 'pos.session'

    def send_session_by_email(self, cr, uid, ids, context=None):
        ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'pos_send_session', 'email_template_send_session')
        return ref and self.pool.get('email.template').send_mail(cr, uid, ref[1], ids[0] , force_send=True) or False

