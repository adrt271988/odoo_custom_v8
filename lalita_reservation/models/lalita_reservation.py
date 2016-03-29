# -*- coding: utf-8 -*-
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

from datetime import datetime
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')

class LalitaFloor(models.Model):
    _name = 'lalita.floor'
    _description = "Floors"
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char('Nombre', size=30, required=True)

class LalitaBed(models.Model):
    _name = 'lalita.bed'
    _description = "Beds"
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char('Nombre', size=30, required=True)
    type = fields.Selection(
        [('1','Sencilla'), ('2','Doble'),('3','Supletoria')],
        'Tipo de Cama')
    room_id = fields.Many2one('lalita.room', 'Habitación')

class LalitaRoom(models.Model):
    _name = 'lalita.room'
    _description = "Rooms"
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char('Nombre',  size=30, required=True)
    bed_count = fields.Integer('N° de Camas')
    floor_id = fields.Many2one('lalita.floor', 'Piso',help="Piso/Planta de la Habitación")
    bed_ids = fields.One2many('lalita.bed', 'room_id', 'Camas en esta habitacion') 


class LalitaReservation(models.Model):
    _name = 'lalita.reservation'
    _description = "Reservations"
    _inherit = ['mail.thread']
    _order = "id desc"
    _rec_name = "name"

    @api.multi
    def send_online_form(self):
        if self.client_ids:
            for client in self.client_ids:
                if client.register_state == 'not_sent':
                    client.write({'register_state':'sent'})

    name = fields.Char(string="Código de Reserva",size=7,select=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Cliente')
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange',
            default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Compañía',
            required=True, change_default=True, readonly=True,
            default=lambda self: self.env['res.company']._company_default_get('lalita.reservation'))
    pricelist_id = fields.Many2one('product.pricelist', string='Tarifa',domain="[('type','=','sale')]")
    arrival_date = fields.Date( string='Fecha de Entrada', required=True)
    out_date = fields.Date( string='Fecha de Salida', required=True)
    state = fields.Selection(
        [('draft','Nuevo'),
        ('open','Abierto'),
        ('done','Cerrado')],
        string='Estado de la Reserva',index=True, default='draft',
        track_visibility='onchange', copy=False)
    notes = fields.Text(string='Observaciones')
    ocupation_days = fields.Integer(
        string='Total Días de Ocupacion',
        compute='_get_ocupation_days')
    berths = fields.Integer('Plazas Reservadas')
    expected_income = fields.Integer(
        string='Estimación de Ingresos',
        compute='_get_expected_income')
    #~ client_ids = fields.Many2many('lalita.guest', 'lalita_reservation_lalita_guest_rel',string="Huéspedes")
    client_ids = fields.One2many('lalita.guest', 'reservation_id',string="Huéspedes")
    room_ids = fields.Many2many('lalita.room', 'lalita_reservation_lalita_room_rel',string="Habitaciones")
    register_ids = fields.One2many('traveler.register','reservation_id',string="Registros de Viajeros")
    sale_id = fields.Many2one('sale.order',string="Pedido",help="Pedido de Ventas Asociado",
        domain="[('state','=','progress')]")
    invoice_ids = fields.One2many('account.invoice','reservation_id',string="Facturas")

    def get_days(self,from_date,to_date):
        fmt = '%Y-%m-%d'
        d1 = datetime.strptime(from_date, fmt)
        d2 = datetime.strptime(to_date, fmt)
        return (d2-d1).days
    
    @api.one
    @api.depends('arrival_date', 'out_date')
    def _get_ocupation_days(self):
        from_date = self.arrival_date
        to_date = self.out_date
        if from_date and to_date:
            days = self.get_days(from_date,to_date)
            if days < 0:
                raise except_orm(_('Advertencia!'), _("La fecha de salida no puede ser menor a la fecha de entrada"))
            self.ocupation_days = str(days)
        
    @api.one
    def _get_expected_income(self):
        self.expected_income = self.ocupation_days * self.berths * 45

    @api.model
    def create(self, values):
        if 'arrival_date' in values and 'out_date' in values:
            if self.get_days(values['arrival_date'],values['out_date']) < 0:
                raise except_orm(_('Advertencia!'), _("La fecha de salida no puede ser menor a la fecha de entrada"))
        if not values.get('name'):
            values['name'] = self.env['ir.sequence'].get('lalita.reservation')
        reservation = super(LalitaReservation, self).create(values)
        reservation.message_post(body=_("Reserva %s creada"%values["name"]))
        return reservation

#TO-DO: Crear un modelo nuevo Huespedes, asociarlos a lalita.reservation como many2many?


class LalitaGuest(models.Model):
    _name = 'lalita.guest'
    _description = "Guests"
    _order = "id desc"

    @api.multi
    def call_traveler_form(self):
        view_form = self.env.ref('lalita_reservation.view_form_traveler_register', False)
        ctx = dict(
            default_guest_id = self.id,
            default_birth_country = self.partner_id.country_id and self.partner_id.country_id.id or False,
            default_first_name = self.partner_id.name,
            default_entry_date = self.arrival_date,
        )
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'traveler.register',
            'views': [(view_form.id, 'form')],
            'view_id': view_form.id,
            'target': 'new',
            'flags': {'form': {'action_buttons': True}},
            'context': ctx,
        }

    partner_id = fields.Many2one('res.partner',string="Huésped")
    reservation_id = fields.Many2one('lalita.reservation',string="Reservación")
    name = fields.Char(string='Nombre',related="partner_id.name",readonly=True)
    phone = fields.Char(string='Teléfono',related="partner_id.phone",readonly=True)
    email = fields.Char(string='Correo',related="partner_id.email",readonly=True)
    guest_state = fields.Selection(
        [('draft','Nuevo'),
        ('confirmed','Confirmado'),
        ('canceled','Cancelado'),
        ('no_show','No Show'),
        ('check_in','Check in'),
        ('early_leave','Salida Temprana'),
        ('check_out','Check out'),],
        string='Estado del Huesped', index=True, default='draft',
        track_visibility='onchange', copy=False)
    arrival_date = fields.Date( string='Fecha de Entrada')
    out_date = fields.Date( string='Fecha de Salida')
    room_id = fields.Many2one('lalita.room',string="Habitación")
    register_state = fields.Selection(
        [('not_sent','No enviado'),
        ('sent','Enviado'),
        ('filled','Registro llenado'),
        ('signed','Firmado e Impreso'),],
        string='Estado Registro Viajero', index=True, default='not_sent',
        track_visibility='onchange', copy=False, readonly=True)
    check = fields.Boolean(string="Seleccione",help="Seleccione para aplicar la acción")
