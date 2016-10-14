# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp.osv import fields, osv
from openerp import models, fields, api, tools, _
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError

class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        products_to_op = []
        if self.project_task_id:
            for line in self.order_line:
                if line.product_id.product_tmpl_id.auto_create_task:
                    vals = {'name': '%s: (%s) %s' % (self.name or '',line.product_id.name, ' a '+self.partner_id.name),
                    'partner_id': self.partner_id.id,
                    'description': line.product_id.product_tmpl_id.description,
                    'project_id': self.project_task_id.id,
                    'company_id': self.company_id.id  }
                    self.env['project.task'].create(vals)
                if line.product_id.product_tmpl_id.auto_create_op:
                    if not self.bom_id:
                        raise except_orm(_('Advertencia!'), _("Debe agregar una lista de materiales"))
                    self.env['mrp.production'].create({
                        'product_id': line.product_id.id,
                        'product_uom': line.product_id.uom_id.id,
                        'origin': self.name,
                        'sale_id': self.id,
                        'bom_id': self.bom_id.id
                        })
                if line.product_id.product_tmpl_id.auto_create_repair:
                    if not self.bom_id:
                        raise except_orm(_('Advertencia!'), _("Debe agregar una lista de materiales"))
                    if self.bom_id.bom_line_ids:
                        lines = []
                        for bom_line in self.bom_id.bom_line_ids:
                            res_change_type = self.env['mrp.repair.line'].onchange_operation_type([bom_line.id], 'add', self.date_order)
                            res_change_product = self.env['mrp.repair.line'].product_id_change(self.env.cr, self.env.uid, [bom_line.id], self.pricelist_id.id, bom_line.product_id.id)
                            values = {
                                'type':'add',
                                'product_id': bom_line.product_id.id,
                                'name': res_change_product['value']['name'],
                                'product_uom': res_change_product['value']['product_uom'],
                                'price_unit': res_change_product['value']['price_unit'],
                                'product_uom_qty': bom_line.product_qty,
                                'to_invoice': res_change_type['value']['to_invoice'],
                                'location_id': res_change_type['value']['location_id'],
                                'location_dest_id': res_change_type['value']['location_dest_id'],
                            }
                            lines.append((0,0,values))
                    self.env['mrp.repair'].create({
                        'product_id': line.product_id.id,
                        'product_uom': line.product_id.uom_id.id,
                        'partner_id': self.partner_id.id,
                        'sale_id': self.id,
                        'location_dest_id': self.warehouse_id.lot_stock_id.id,
                        'operations': lines,
                        })
        res = super(sale_order, self).action_button_confirm()
        return True

    project_task_id = fields.Many2one(comodel_name='project.project', string='Taller',help="Dejar vacio si la orden no va a generar una tarea en el taller")
    bom_id = fields.Many2one(comodel_name='mrp.bom', string='Lista de Materiales',help="Lista de materiales asociada a la orden")




class project_task(models.Model):
    _inherit = "project.task"

    sale_line_id = fields.Many2one(comodel_name='sale.order.line', string='Presupuesto', readonly=True)




class product_template(models.Model):
    _inherit = "product.template"

    auto_create_task =  fields.Boolean('Crear tarea automaticamente', help="Tick this option if you want to create a task automatically each time this product is sold")
    auto_create_op =  fields.Boolean('Crear Orden de Producción', help="Marque esta opción si quiere crear una orden de producción a partir de este servicio")
    auto_create_repair =  fields.Boolean('Crear Orden de Reparación', help="Marque esta opción si quiere crear una orden de reparación a partir de este servicio")


class mrp_production(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Pedido',
        readonly=True
        )

class mrp_repair(models.Model):
    _inherit = 'mrp.repair'

    sale_id = fields.Many2one(
        'sale.order',
        string='Pedido',
        readonly=True
        )


    #~ def action_button_confirm(self, cr, uid, ids, context=None):
        #~ if not context:
            #~ context = {}
        #~ assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        #~ self.signal_workflow(cr, uid, ids, 'order_confirm')
        #~ if context.get('send_email'):
            #~ self.force_quotation_send(cr, uid, ids, context=context)
        #~ return True



#~
#~ class res_ship(models.Model):
    #~ _name = "res.ship"
    #~ _description = "Embarcaciones"
#~
#~
    #~ @api.model
    #~ def default_get(self, fields):
        #~ res = super(res_ship, self).default_get(fields)
        #~ if self._context.get('partner_id'):
            #~ partner_id = self._context.get('partner_id')
            #~ partner = self.env['res.partner'].browse(partner_id)
            #~ if self._context.get('ship_rel') == 'PR':
                #~ res['customer_id'] = partner_id
            #~ elif self._context.get('ship_rel') == 'AU':
                #~ res.update({'autorized_ids': [(0,0,{'partner_id':partner_id,
                                                    #~ 'relation_type':'autorized',
                                                    #~ 'email': partner.email,
                                                    #~ 'phone': partner.phone and partner.phone or partner.mobile
                                                    #~ })]})
        #~ return res
#~
    #~ @api.model
    #~ def create(self, values):
        #~ res = super(res_ship, self).create(values)
        #~ if values['autorized_ids'][0][2]:
            #~ for i in values['autorized_ids']:
                #~ ship = i[2]['ship_partner_id']
                #~ partner = self.env['res.partner'].browse(i[2]['partner_id'])
                #~ if i[2]['relation_type'] == 'autorized':
                    #~ partner.write({'autorized_ids': [(0,0,{'parent_id': partner.id,'ship_id': ship,
                                                           #~ 'ship_rel':'autorized'})]})
                #~ elif i[2]['relation_type'] == 'administer':
                    #~ partner.write({'autorized_ids': [(0,0,{'parent_id': partner.id,'ship_id': ship,
                                                           #~ 'ship_rel':'administer'})]})
        #~ return res
#~
    #~ @api.multi
    #~ def write(self, values):
        #~ print '************',values
        #~ if values.get('autorized_ids'):
            #~ for lis in values['autorized_ids']:
                #~ if lis[0] == 0: #registro agregado
                    #~ print 'agregando'
                    #~ rel = lis[2]['relation_type'] == 'administer' and 'administer' or lis[2]['relation_type'] == 'autorized' and 'autorized' or ''
                    #~ partner = self.env['res.partner'].browse(lis[2]['partner_id'])
                    #~ partner.write({'autorized_ids': [(0,0,{'parent_id': partner.id,'ship_id': self.id,
                                                           #~ 'ship_rel': rel})]})
                #~ if lis[0] == 2: #registro eliminado
                    #~ print 'eliminando'
                    #~ partner = self.env['res.ship.autorized'].browse(lis[1])
                    #~ for aut in partner.partner_id.autorized_ids:
                        #~ if aut.ship_id.id == partner.ship_partner_id.id and partner.relation_type == aut.ship_rel:
                            #~ aut.unlink()
        #~ return super(res_ship, self).write(values)
#~
#~
#~
#~
    #~ name =  fields.Char(
            #~ string='Nombre', size=128, required=True, readonly=True,
            #~ states={'draft': [('readonly', False)]},
            #~ help="Descripción de la Embarcación")
    #~ image = fields.Binary(
            #~ string="Image")
    #~ image_medium = fields.Binary(
                   #~ compute='_get_medium_image',
                   #~ inverse='_set_image_from_medium',
                   #~ string="Medium-sized image", store=True)
    #~ image_small =  fields.Binary(
                   #~ compute='_get_small_image',
                   #~ inverse='_set_image_from_small',
                   #~ string="Small-sized image", type="binary", store=True)
    #~ category_id =  fields.Many2many(
                   #~ comodel_name='res.ship.category',
                   #~ relation='ship_category',
                   #~ column1='ship_id', column2='category_id', readonly=True,
                   #~ states={'draft': [('readonly', False)]})
    #~ brand_id = fields.Many2one(
            #~ 'res.ship.brand', string='Marca', readonly=True,
            #~ states={'draft': [('readonly', False)]},
            #~ help="Marca")
    #~ model_id = fields.Many2one(
            #~ 'res.ship.model', string='Modelo',readonly=True,
            #~ states={'draft': [('readonly', False)]},
            #~ help="Modelo")
    #~ customer_id = fields.Many2one(
            #~ 'res.partner', string='Propietario',readonly=True,
            #~ states={'draft': [('readonly', False)]},
            #~ help="Propietario de la embarcación")
    #~ autorized_ids = fields.One2many(
            #~ 'res.ship.autorized', inverse_name='ship_partner_id',
            #~ string='Autorizados',readonly=True,
            #~ states={'draft': [('readonly', False)],'done': [('readonly', False)]},
                    #~ help="Personal autorizado")
    #~ type = fields.Selection([
        #~ ('L', 'Lancha'),
        #~ ('V', 'Velero'),
        #~ ('Y', 'Yate'),
        #~ ('D', 'Dinghy'),
        #~ ], string='Tipo',readonly=True,
        #~ states={'draft': [('readonly', False)]},
        #~ help="Tipo de embarcación")
    #~ state = fields.Selection([
        #~ ('draft', 'En proceso'),
        #~ ('done', 'Operativa'),
        #~ ('cancel', 'Inactiva'),
        #~ ], string='Status',readonly=True, default='draft',
        #~ help="""Status de la embarcación:
                #~ - En proceso: status inicial cuando la embarcación se encuentra en proceso de registro.
                #~ - Operativa: La embarcación se encuentra registrada en el sistema.
                #~ - Inactiva: La embarcación ya no esta disponible.""")
    #~ address = fields.Char(
        #~ string='Ubicación',readonly=True,
        #~ states={'draft': [('readonly', False)]},
        #~ help="")
    #~ color = fields.Integer(
        #~ string='Color',readonly=True,
        #~ states={'draft': [('readonly', False)]},
        #~ default=1)
    #~ feets = fields.Float(
        #~ string='Pies',readonly=True,
        #~ states={'draft': [('readonly', False)]},
        #~ help="Tamaño en (Pies)")
    #~ year = fields.Integer(
        #~ string='Año', size=4,readonly=True,
        #~ states={'draft': [('readonly', False)]},
        #~ help="Año de la embarcación")
    #~ note = fields.Text(
        #~ string='Notas',
        #~ help="Información adicional de la embarcación")
