# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.osv import osv, fields
import datetime

class sinsumos_res_partner(osv.osv):
    _inherit = "res.partner"

    #~ def button_check_vat(self, cr, uid, ids, context=None):
        #~ partner = self.browse(cr, uid, ids[0])
        #~ cr.execute(""" SELECT id,vat from res_partner WHERE vat = '%s' """%partner.vat)
        #~ query = cr.dictfetchone()
        #~ print '********',query
        #~ super(sinsumos_res_partner, self).button_check_vat(cr, uid, ids, context = context)
        #~ return True
