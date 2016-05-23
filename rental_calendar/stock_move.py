from openerp.tools.translate import _
from openerp.osv import osv, fields

class warehouse_calendar_stock_move(osv.osv):
    _inherit = "stock.move"

    _columns = {
                'picking_partner': fields.related('picking_id', 'partner_id', type='many2one', relation='res.partner', string='Partner'),
    }
