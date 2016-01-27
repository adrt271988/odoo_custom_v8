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
                    if rental.start_order_id not in sales:
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
