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


from openerp.osv import osv
from openerp.tools.translate import _

class ProductBarcodeReport(osv.AbstractModel):
    _name = 'report.product_barcode_printer.report_product_barcode'
    
    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        product_obj = self.pool['product.product']
        docs = product_obj.browse(cr, uid, ids, context=context)
        
        report = report_obj._get_report_from_name(cr, uid, 'product_barcode_printer.report_product_barcode')
        docargs = {
            'doc_ids': ids,
            'doc_model': report.model,
            'docs': docs,
        }
        return report_obj.render(cr, uid, ids, 'product_barcode_printer.report_product_barcode', docargs, context=context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

