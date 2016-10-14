# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    "name" : "Adaptación de Servicios",
    "version" : "1.0",
    "author" : "Luis Torres",
    "website" : "www.onawoo.com.ve",
    "category": "Sales",
    "summary": "Creación de tarea y orden de producción a partir del pedido d venta.",
    "description": """

                   """,
    "depends" : [
                "sale_mrp","project","mrp_repair"
                ],
    'data': [
        "view/ship_service_view.xml"
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
