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

from lxml import etree
from datetime import datetime
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError

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
    _order = "room_id desc"
    _rec_name = "name"

    name = fields.Char('Nombre', size=30, required=True)
    type = fields.Selection(
        [('1','Sencilla'), ('2','Doble'),('3','Supletoria')],
        'Tipo de Cama')
    room_id = fields.Many2one('lalita.room', 'Habitación')

    _sql_constraints = [
        ('name_uniq', 'unique(name)',
            'El nombre de la cama ya existe!'),
    ]

class LalitaRoom(models.Model):
    _name = 'lalita.room'
    _description = "Rooms"
    _order = "id desc"
    _rec_name = "name"

    @api.multi
    @api.depends('bed_ids')
    def _get_bed_count(self):
        for room in self:
            if room.bed_ids:
                room.bed_count = sum([int(bed.type) for bed in room.bed_ids])

    name = fields.Char('Nombre',  size=30, required=True)
    bed_count = fields.Integer('N° de Plazas', compute='_get_bed_count')
    floor_id = fields.Many2one('lalita.floor', 'Piso',help="Piso/Planta de la Habitación")
    bed_ids = fields.One2many('lalita.bed', 'room_id', 'Camas en esta habitacion') 


class LalitaReservation(models.Model):
    _name = 'lalita.reservation'
    _description = "Reservations"
    _inherit = ['mail.thread']
    _order = "id desc"
    _rec_name = "name"

    @api.one
    def cancel_reservation(self):
        self.state = "cancel"
    
    @api.one
    def close_reservation(self):
        self.state = "done"
        
    @api.one
    def send_online_form(self):
        if self.client_ids:
            for client in self.client_ids:
                if client.check:
                    if client.register_state == 'not_sent':
                        client.register_state = 'sent'
                    client.check = False
                        
    @api.one
    def check_in(self):
        if self.client_ids:
            for client in self.client_ids:
                if client.check:
                    if client.guest_state == 'confirmed':
                        traveler_values = {
                                    'doc_number': client.partner_id.doc_number and client.partner_id.doc_number or '',
                                    'doc_type': client.partner_id.doc_type and client.partner_id.doc_type or '',
                                    'last_name1': client.partner_id.last_name1 and client.partner_id.last_name1 or '',
                                    'last_name2': client.partner_id.last_name2 and client.partner_id.last_name2 or '',
                                    'first_name': client.partner_id.first_name and client.partner_id.first_name or '',
                                    'gender': client.partner_id.gender and client.partner_id.gender or '',
                                    'birth_date': client.partner_id.birth_date and client.partner_id.birth_date or '',
                                    'birth_country': client.partner_id.country_id and client.partner_id.country_id.id or '',
                                    'reservation_id': self.id
                                        }
                        self.env['traveler.register'].create(traveler_values)
                        client.arrival_date = datetime.today()
                        client.guest_state = 'check_in'
                        client.register_state = 'filled'
                    client.check = False

    @api.one
    def change_state(self):
        if self.client_ids:
            for client in self.client_ids:
                if client.check:
                    if self.change_guest_state == "check_out":
                        client.out_date = datetime.today()
                    client.guest_state = self.change_guest_state
                client.check = False

    @api.multi
    @api.depends('room_ids')
    def _get_total_berths(self):
        for reservation in self:
            if reservation.room_ids:
                reservation.total_berths = sum([room.bed_count for room in reservation.room_ids])
                
    @api.multi
    @api.depends('total_berths','client_ids')
    def _get_available_berths(self):
        for reservation in self:
            guests = 0
            if reservation.client_ids:
                guests = len([x.id for x in reservation.client_ids])
            available = reservation.total_berths - guests
            if available < 0:
                raise ValidationError(_("No hay mas plazas disponibles!!!"))
            reservation.available_berths = available

    name = fields.Char(string="Código de Reserva",size=7,select=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Cliente')
    user_id = fields.Many2one('res.users', string='Responsable', track_visibility='onchange',
            default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Compañía',
            required=True, change_default=True, readonly=True,
            default=lambda self: self.env['res.company']._company_default_get('lalita.reservation'))
    pricelist_id = fields.Many2one('product.pricelist', string='Tarifa',
                        domain="[('type','=','sale')]",readonly=True)
    arrival_date = fields.Datetime( string='Fecha de Entrada', required=True)
    out_date = fields.Datetime( string='Fecha de Salida', required=True)
    state = fields.Selection(
        [('draft','Borrador'),
        ('open','Confirmada'),
        ('cancel','Cancelada'),
        ('done','Finalizado')],
        string='Estado de la Reserva',index=True, default='draft',
        track_visibility='onchange', copy=False)
    notes = fields.Text(string='Observaciones')
    ocupation_days = fields.Integer(
        string='Total Días de Ocupacion',
        compute='_get_ocupation_days')
    berths = fields.Integer('Número de Plazas',readonly=True)
    total_berths = fields.Integer(string='Total de Plazas',readonly=True,
                        compute='_get_total_berths',help="Total de plazas a reservar en el establecimiento")
    expected_income = fields.Float(
        string='Estimación de Ingresos',readonly=True)
    client_ids = fields.One2many('lalita.guest', 'reservation_id',string="Huéspedes")
    room_ids = fields.Many2many('lalita.room', 'lalita_reservation_lalita_room_rel',string="Habitaciones")
    register_ids = fields.One2many('traveler.register','reservation_id',string="Registros de Viajeros")
    sale_id = fields.Many2one('sale.order',string="Pedido",help="Pedido de Ventas Asociado",
        domain="[('state','not in',['draft','sent','cancel','waiting_date'])]")
    invoice_ids = fields.One2many('account.invoice','reservation_id',string="Facturas")
    change_guest_state = fields.Selection(
        [('draft','Nuevo'),
        ('confirmed','Confirmado'),
        ('canceled','Cancelado'),
        ('no_show','No Show'),
        ('early_leave','Salida Temprana'),
        ('check_out','Check out'),],
        string='Estado del Huesped', index=True, default='draft',
        track_visibility='onchange', copy=False,
        help="Seleccione los huéspedes y luego cambie este campo para asignarles el estatus que desee")
    available_berths = fields.Integer(string='Plazas Restantes', compute='_get_available_berths',
                                        help="Plazas restantes en la Reserva")

    @api.onchange('sale_id')
    def onchange_sale_id(self):
        sale_id = self.sale_id
        if sale_id:
            self.partner_id = sale_id.partner_id
            self.arrival_date = sale_id.arrival_date
            self.out_date = sale_id.departure_date
            self.berths = sale_id.berths
            self.pricelist_id = sale_id.pricelist_id
            self.expected_income = sale_id.amount_total

    @api.onchange('client_ids')
    @api.depends('total_berths')
    def onchange_client_ids(self):
        msg = {}
        count = len([x.id for x in self.client_ids])
        if count > self.total_berths:
            msg = {'title': _('Advertencia!'), 'message' : 'Existen mas huéspedes que plazas disponibles en esta reserva'}
        return {'warning': msg}

    def get_days(self,from_date,to_date):
        fmt = '%Y-%m-%d %H:%M:%S'
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

class LalitaGuest(models.Model):
    _name = 'lalita.guest'
    _description = "Guests"
    _order = "id desc"

    @api.multi
    def set_leaving_motive(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        view_form = self.env.ref('lalita_reservation.leaving_motive_form', False)
        return {
            'name': _('Motivo de Salida'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'leaving.motive',
            'views': [(view_form.id, 'form')],
            'view_id': view_form.id,
            'target': 'new'
        }

    @api.multi
    def call_traveler_form(self):
        view_form = self.env.ref('lalita_reservation.view_form_traveler_register', False)
        ctx = dict(
            default_guest_id = self.id,
            default_reservation_id = self.reservation_id and self.reservation_id.id or False,
            default_birth_country = self.partner_id.country_id and self.partner_id.country_id.id or False,
            default_first_name = self.partner_id.first_name,
            default_doc_number = self.partner_id.doc_number,
            default_doc_type = self.partner_id.doc_type,
            default_document_date = self.partner_id.document_date,
            default_birth_date = self.partner_id.birth_date,
            default_gender = self.partner_id.gender,
            default_last_name1 = self.partner_id.last_name1,
            default_last_name2 = self.partner_id.last_name2,
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

    partner_id = fields.Many2one('res.partner',string="Nombre")
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
        track_visibility='onchange', copy=False, readonly=True)
    arrival_date = fields.Datetime( string='Fecha de Entrada')
    out_date = fields.Datetime( string='Fecha de Salida')
    room_id = fields.Many2one('lalita.room',string="Habitación")
    register_state = fields.Selection(
        [('not_sent','No enviado'),
        ('sent','Enviado'),
        ('filled','Registro llenado'),
        ('signed','Firmado e Impreso'),],
        string='Estado Registro Viajero', index=True, default='not_sent',
        track_visibility='onchange', copy=False, readonly=True)
    check = fields.Boolean(string="Seleccione",help="Seleccione para aplicar la acción",default=False)
    leaving_motive = fields.Text(string="Motivo del Retiro", help="Motivo de la Salida del Huésped")

