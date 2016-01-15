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
    'name': 'Custom Security Module',
    'category': '', 
    'version': '1.0',
    'description': """ 
Custom Security Module
====================================================
* Create and set new user rights / user groups.
====================================================
How to use it
====================================================
* Once it’s installed, the module creates two groups: Bookkeeper and View. Just have to create the users and asign them to the groups that you want
* To create the Users go to Settings > Users > Users, fill the user attributes, in Access Rights tab, in section “Other” you will find the check marks to associate the user with the new groups
* Log in the with the new users (Bookkeeper or View) to check them
    """,
    'author': 'Alexander Rodriguez',
    'website': '',
    'depends': ['base','hr','project','purchase','account_voucher','knowledge','document','mail','sales_team','marketing','website','website_mail','sale','marketing_campaign'],
    'data': [
            'security/employee_messaging.xml',
            'security/bookkeeper.xml',
            'security/view.xml',
            'security/ir.model.access.csv',
            'project_view.xml',
            'account_view.xml',
            'res_users_view.xml',
            'account_invoice_view.xml',
            'res_partner_view.xml',
            'knowledge_view.xml',
            'mail_view.xml',
    ],
    'qweb' : [
        "static/src/xml/base.xml",
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
