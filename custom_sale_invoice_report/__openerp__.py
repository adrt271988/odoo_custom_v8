# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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


{
    'name': 'ARA de Ventas',
    'category': 'Account', 
    'version': '1.0',
    'description': """ 
Analisis de Facturas ARA
====================================================
* Se agrega un nuevo menu en modulo informes (Informes/Ventas/Analisis de Facturas ARA).
* Se elimina el filtro de Proveedores, se coloca por defecto el filtro de Clientes.
* Se agrega una nueva clasificacion llamada Categoria Padre, la cual permite ver la sumatoria de montos de las facturas por categorias de producto tipo vista.
* Se agrega un nuevo de grupo de usuarios Informes avanzados/Analisis de facturas ARA. Los usuarios asociados a este grupo podran visualizar el reporte.
* Se agrega un nueva Regla de Registro, con la finalidad de que los vendedores solo puedan ver la informacion relacionada a su equipo de ventas.
    """,
    'author': 'Alexander Rodriguez',
    'website': '',
    'depends': ['base','sale'],
    'data': [
            'report/sale_invoice_report_view.xml',
            'security/res_groups.xml',
            'security/rules.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
