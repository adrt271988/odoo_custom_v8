# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.osv import osv, fields
import datetime

class rental_calendar_sale_rental(osv.osv):
    _inherit = "sale.rental"

    def rental_reminder(self, cr, uid, context=None):
        fmt = "%Y-%m-%d"
        sales = []
        rental_ids = self.search(cr, uid, [])
        if rental_ids:
            #Obtenemos los pedidos de venta a evaluar
            for rental in self.browse(cr, uid, rental_ids, context):
                if rental.state == 'out':
                    if rental.start_order_id.id not in sales:
                        sales.append(rental.start_order_id.id)
            #Enviamos la notificacion por pedido
            for sale in self.pool.get('sale.order').browse(cr, uid, sales, context):
                end_date = datetime.datetime.strptime(sale.global_end_date,fmt)
                diff = end_date - datetime.datetime.now()
                ref = ()
                if diff.days == 1:
                    ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'rental_calendar', 'email_template_rental_reminder')
                if ref:
                    self.pool.get('email.template').send_mail(cr, uid, ref[1], rental.id , force_send=True)
        return True

    def create(self, cr, uid, vals, context=None):
        if vals.get('start_order_line_id', False):
            line_obj = self.pool.get('sale.order.line')
            line = line_obj.browse(cr, udi, vals['start_order_line_id'])
            vals.update({'non_rel_sale_id': line.sale_id.id , 'non_rel_partner_id': line.sale_id.partner_id.id})
        return super(rental_calendar_sale_rental, self).create(cr, uid, default, context=context)

    _columns = {
                'non_rel_partner_id': fields.many2one('res.partner','Partner', help="Non Related Partner Field"),
                'non_rel_sale_id': fields.many2one('sale.order','Sale Order', help="Non Related Sale Order Field"),
    }
