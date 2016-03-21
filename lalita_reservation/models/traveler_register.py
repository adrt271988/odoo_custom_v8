# -*- encoding: utf-8 -*-
##############################################################################
#
#    Custom module for Odoo
#    @author Alexander Rodriguez <adrt271988@gmail.com>
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
from openerp import models, fields, api, _

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')

class TravelerRegister(models.Model):
    _name = 'traveler.register'
    _description = "Traveler Registration"
    _inherit = ['mail.thread']
    _order = "id desc"
    _rec_name = "code"

    @api.multi
    def send_register(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        template = self.env.ref('lalita_reservation.email_template_traveler_register', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='traveler.register',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            mark_register_as_sent = True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
        
    def print_register(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        self.write({'state':'printed'})
        return self.env['report'].get_action(self, 'lalita_reservation.report_traveler_register')
        
    @api.model
    def create(self, values):
        if not values.get('code'):
            values['code'] = self.env['ir.sequence'].get('traveler.register')
        self.env['mail.thread'].message_post(body=_("Registro de viajeros %s creado"%values["code"]))
        self.message_post(body=_("Registro de viajeros %s creado"%values["code"]))
        return super(TravelerRegister, self).create(values)

    code = fields.Char('Código', size=4, help="Código de Identificación del Registro", select=True, readonly=True)
    doc_number = fields.Char('Documento Identificación', size=14,required=True,help="Número de Documento de Identidad")
    doc_type = fields.Selection(
            [('D','DNI Españoles'),
            ('P','Pasaportes'),
            ('C ','Permiso de conducir español'),
            ('I','Carta o documento de identidad'),
            ('X','Permiso de residencia UE'),
            ('N','Permiso de residencia español')],
            'Tipo de Documento', size=1, required=True)
    document_date = fields.Date('Fecha de Expedición', required=True)
    last_name1 = fields.Char('Primer Apellido', size=30, required=True)
    last_name2 = fields.Char('Segundo Apellido', size=30, required=True)
    first_name = fields.Char('Nombre', size=30, required=True)
    gender = fields.Selection([('F','Femenino'),('M','Masculino')],'Sexo',size=1,required=True)
    birth_date = fields.Date('Fecha de Nacimiento', required=True)
    birth_country = fields.Char('Pais de Nacionalidad', size=21, required=True)
    entry_date = fields.Date('Fecha de Entrada', required=True, default = lambda self: fields.Date.context_today(self))
    #~ sent = fields.Boolean('Enviado?', default=False)
    reservation_id = fields.Many2one('lalita.reservation', string='Cliente')
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange',
            default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Compañía',
            required=True, change_default=True, readonly=True,
            default=lambda self: self.env['res.company']._company_default_get('traveler.register'))
    state = fields.Selection(
        [('draft','Nuevo'),
        ('printed','Impreso'),
        ('sent','Enviado'),],
        string='Estatus', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * 'Nuevo' Registro por imprimir.\n"
             " * 'Impreso' Cuando se ha impreso el formulario de Registro de Viajeros.\n"
             " * 'Enviado' Cuando se ha enviado el Registro de Viajeroa la Guardia.")

class mail_compose_message(models.Model):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self):
        context = self._context
        if context.get('default_model') == 'traveler.register' and \
                context.get('default_res_id') and context.get('mark_register_as_sent'):
            register = self.env['traveler.register'].browse(context['default_res_id'])
            register = register.with_context(mail_post_autofollow=True)
            register.write({'state': 'sent'})
            register.message_post(body=_("Registro de Viajero %s Enviado"%register.code))
        return super(mail_compose_message, self).send_mail()
