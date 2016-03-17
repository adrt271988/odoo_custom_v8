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
from openerp import models, fields, api

class LalitaBed(models.Model):
    _name = 'lalita.bed'
    _description = "Beds"
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char('Nombre', size=30, required=True)
    type = fields.Selection(
        [('1','Sencilla'), ('2','Doble')],
        'Tipo de Cama')
    room_id = fields.Many2one('lalita.room', 'Habitación') 

    class LalitaRoom(models.Model):
    _name = 'lalita.room'
    _description = "Rooms"
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char('Nombre',  size=30, required=True)
    bed_count = fields.Integer('N° de Camas')
    bed_ids = fields.One2many('lalita.bed', 'room_id', 'Camas en esta habitacion') 


    class LalitaReservation(models.Model):
    _name = 'lalita.reservation'
    _description = "Reservations"
    _order = "id desc"
    _rec_name = "name"

    name = fields.Char(string="Código de Reserva")
    partner_id = fields.Many2one('res.partner', string='Cliente')
    pricelist_id = fields.Many2one('product.pricelist', string='Tarifa')
    arrival_date = fields.Date( string='Fecha de Entrada', required=True)
    out_date = fields.Date( string='Fecha de Salida', required=True)
    state = fields.Selection(
        [('draft','Nuevo'),
        ('open','Abierto'),
        ('done','Cerrado')],
        'Estado de la Reserva')
    notes = fields.Text(string='Observaciones')
    ocupation_days = fields.Integer(
        string='Total Días de Ocupacion',
        compute='_get_ocupation_days')
    berths = fields.Integer('Plazas Reservadas')
    expected_income = fields.Integer(
        string='Estimación de Ingresos',
        compute='_get_expected_income')
    client_ids = fields.Many2many('res.partner', 'lalita_reservation_res_partner_rel',string="Huéspedes")
    room_ids = fields.Many2many('lalita.room', 'lalita_reservation_lalita_room_rel')
    #	quotations_ids = fields.Many2many('sale.order', 'group_quotations')

    @api.one
    def _get_ocupation_days(self):
        fmt = '%Y-%m-%d'
        from_date = self.arrival_date
        to_date = self.out_date
        d1 = datetime.strptime(from_date, fmt)
        d2 = datetime.strptime(to_date, fmt)
        self.ocupation_days = str((d2-d1).days)
        
    @api.one
    def _get_expected_income(self):
        self.expected_income = self.ocupation_days * self.berths * 45
