from openerp.tools.translate import _
from openerp.osv import osv, fields

class rental_calendar_product_product(osv.osv):
    _inherit = "product.product"

    _columns = {
                'delay': fields.integer('Dias de Retraso',help="Dias de retraso permitidos"),
    }
