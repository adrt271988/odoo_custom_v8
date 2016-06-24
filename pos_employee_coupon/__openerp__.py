# -*- encoding: utf-8 -*-
##############################################################################
#
#    Custom module for Odoo
#    @author Onawoo Soluciones C.A.
#            Alexander Rodriguez <adrt271988@gmail.com>
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
    'name': 'TPV Vales de Empleado',
    'version': '0.0.1',
    'author': 'Onawoo Soluciones C.A., Alexander Rodriguez <adrt271988@gmail.com>',
    'summary': 'Vales de Empleado desde TPV',
    'description': """ 
Vales de Empleado desde el TPV
==========================================================================================================
* Creación automática de Vales de Empleado
* Se crearán los vales si el empleado paga una compra en el TPV con diario de Débito
* Se debe configurar el campo Direccion particular en la ficha del empleado con el partner correspondiente
* Creación de Regla Salariales para descontar los vales al empleado en el recibo de nómina
    """,
    'category': 'Point Of Sale',
    'website': 'https://www.onawoo.com.ve',
    'depends': ['pos_debt_notebook','hr_payroll'],
    'data': [
            'data/pos_coupon_sequence.xml',
            'data/hr_payroll_data.xml',
            'view/pos_coupon_view.xml',
            'view/hr_employee_view.xml',
            'view/hr_payslip_view.xml',
        ],
    'installable': True,
}
