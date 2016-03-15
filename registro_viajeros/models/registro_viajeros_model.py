# -*- coding: utf-8 -*-
from openerp import models, fields
class RegistroViajeros(models.Model):
	_name = 'registro_viajeros'
	id_numero = fields.Char('Número de Documento de Identidad', size=14,required=True)
	id_tipo = fields.Selection(
	[('D','DNI Españoles'),
	('P','Pasaportes'),
	('C ','Permiso de conducir español'),
	('I','Carta o documento de identidad'),
	('X','Permiso de residencia UE'),
	('N','Permiso de residencia español')],
	'Tipo de Documento', size=1, required=True)
	fecha_expedicion = fields.Date('Fecha de Expedición', required=True)
	primer_apellido = fields.Char('Primer Apellido', size=30, required=True)
	segundo_apellido = fields.Char('Segundo Apellido', size=30, required=True)
	nombre = fields.Char('Nombre', size=30, required=True)
	sexo = fields.Selection([('F','Femenino'),('M','Masculino')],'Sexo',size=1,required=True)
	fecha_nacimiento = fields.Date('Fecha de Nacimiento', required=True)
	nacionalidad = fields.Char('Pais de Nacionalidad', size=21, required=True)
	fecha_entrada = fields.Date('Fecha de Entrada', required=True)
	enviado = fields.Boolean('Enviado?', default=False)
