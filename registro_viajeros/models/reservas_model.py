# -*- coding: utf-8 -*-
from datetime import datetime
from openerp import models, fields, api

class Bed(models.Model):
	_name = 'bed'
	nombre = fields.Char('Nombre', size=30, required=True)
	tipo = fields.Selection(
		[('1','Sencilla'), ('2','Doble')],
		'Tipo de Cama')
	room_id = fields.Many2one('room', 'Número de Habitacion') 

class Room(models.Model):
	_name = 'room'
	nombre = fields.Char('Nombre',  size=30, required=True)
	plazas = fields.Integer('N Camas')
	beds = fields.One2many('bed', 'room_id', 'Camas en esta habitacion') 


class Reservas(models.Model):
	_name = 'reservas'
	partner_id = fields.Many2one('res.partner', 'Cliente')
	tarifa_id = fields.Many2one('product.pricelist', 'Tarifa')
	fecha_entrada = fields.Date('Fecha de Entrada', required=True)
	fecha_salida = fields.Date('Fecha de Salida', required=True)
	state = fields.Selection(
		[('draft','New'),
		('open','Started'),
		('done','Closed')],
		'Estado de la Reserva')
	observaciones = fields.Text('Observaciones')
	ocupacion_dias = fields.Integer(
		'Total Días de Ocupacion',
		compute='_ocupacion_dias')
	plazas = fields.Integer('Plazas Reservadas')
	estimacion_ingresos = fields.Integer(
		'Estimación de Ingresos',
		compute='_estimacion_ingresos')
	huespedes_ids = fields.Many2many('res.partner', 'huesped')
	rooms_ids = fields.Many2many('room', 'reservas_habitacion')
#	quotations_ids = fields.Many2many('sale.order', 'group_quotations')
	
	@api.one
	def _ocupacion_dias(self):
		
		fmt = '%Y-%m-%d'
		from_date = self.fecha_entrada
		to_date = self.fecha_salida
		
		d1 = datetime.strptime(from_date, fmt)
		d2 = datetime.strptime(to_date, fmt)
		
		self.ocupacion_dias = str((d2-d1).days)
		
	@api.one
	def _estimacion_ingresos(self):
		
		self.estimacion_ingresos = self.ocupacion_dias * self.plazas * 45