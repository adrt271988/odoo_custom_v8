from openerp.tools.translate import _
from openerp.osv import osv, fields

class project_sequence_project_project(osv.osv):
    _inherit = "project.project"

    _columns = {
                'code': fields.char('VDMi Project ID', copy=False, readonly=True, states={'draft': [('readonly', False)], 'template': [('readonly',False)], 'open': [('readonly',False)]}, select=True),
    }

    def _get_next_seq(self, cr, uid, context=None):
        last_id = 0
        get_count = self.search(cr, uid, [(1, '=', 1)], order='id')
        if get_count:
            for item in self.browse(cr, uid, get_count, context):
                sec_num = int(item.code) + 1
                last_id = sec_num
        else:
            last_id = 1
        seq = last_id
        code = str(seq).rjust(12, '0')
        return code 

    def get_code(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'code': self.pool.get('ir.sequence').get(cr, uid, 'project.project', context=context) or ''})
        #~ self.write(cr, uid, ids, {'code': self._get_next_seq(cr, uid, context)})
        return True

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for rec in self.browse(cr, uid, ids, context):
            name = rec.code is not False and '%s / %s'%(rec.code,rec.name) or '%s'%rec.name
            res.append((rec.id, name))
        return res
