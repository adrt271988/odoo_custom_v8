from openerp.tools.translate import _
from openerp.osv import osv, fields
import datetime

class rental_calendar_sale_rental(osv.osv):
    _inherit = "sale.rental"

    def rental_reminder(self, cr, uid, context=None):
        fmt = "%Y-%m-%d"
        rental_ids = self.search(cr, uid, [])
        if rental_ids:
            for rental in self.browse(cr, uid, rental_ids, context):
                if rental.state == 'out':
                    end_date = datetime.datetime.strptime(rental.end_date,fmt)
                    diff = end_date - datetime.datetime.now()
                    ref = ()
                    if diff.days == 1:
                        ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'rental_calendar', 'email_template_rental_reminder')
                    if datetime.datetime.now() > end_date:
                        diff_2 = datetime.datetime.now() - end_date
                        if diff_2.days >= rental.rental_product_id.delay:
                            ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'rental_calendar', 'email_template_rental_delay')
                    if ref:
                        print '****************',ref[1]
                        self.pool.get('email.template').send_mail(cr, uid, ref[1], rental.id , force_send=True)
        return True
