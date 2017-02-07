# -*- encoding: utf-8 -*-
from openerp import netsvc
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime, date, timedelta
from openerp.osv import osv
from openerp.exceptions import except_orm
import time
import calendar
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
import xlwt
import base64
import re
from cStringIO import StringIO

class AccountingReportLkt(models.TransientModel):
    _name = 'accounting.report.lkt'

    @api.model
    def is_zero(self, account, balances_by_period):
        """ Función para verificar que la cuenta posee balance en cero
            para todos los peridos"""
        currency_obj = self.pool.get('res.currency')
        count = 0
        #Recorremos el diccionario
        for i in balances_by_period:
            if currency_obj.is_zero(self.env.cr, self.env.uid, account.company_id.currency_id, balances_by_period[i]):
                count += 1
        return count == len(balances_by_period) and True or False

    @api.model
    def get_balance(self, debit, credit):
        balance = 0.0
        if debit > credit:
            balance = debit - credit
        elif credit > debit:
            balance = credit - debit
            balance *= -1
        return balance

    @api.multi
    def generate(self):
        ##Obtenemos las lineas del reporte
        lines = []
        year = self.period_id.fiscalyear_id.name
        account_obj = self.pool.get('account.account')
        report_obj = self.pool.get('account.financial.report')
        report_ids = report_obj.search(self.env.cr, self.env.uid, [('parent_id','=',self.financial_report_id.id),('type','!=','account_report')],order="sequence asc")
        move_line_obj = self.env['account.move.line']
        period_obj = self.env['account.period']

        workbook = xlwt.Workbook(encoding="utf-8")
        name = 'Balance de Situacion'
        today = datetime.today().strftime("%d-%m-%Y")
        company = self.env['res.users'].browse(self.env.uid).company_id.name
        header_style1 = xlwt.easyxf('font: bold on, height 160; align: wrap on, horiz center, vert center;')
        header_style2 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour pale_blue, pattern_back_colour pale_blue; font: bold on, height 160; align: wrap on, horiz center, vert center;')
        header_style3 = xlwt.easyxf('pattern: pattern solid, pattern_fore_colour gray25, pattern_back_colour gray25; font: bold on, height 160; align: wrap on, horiz center, vert center;')
        title_style = xlwt.easyxf('font: bold on, height 160; align: wrap on, horiz center, vert center; border: top thick, right thick, bottom thick, left thick;')
        base_style = xlwt.easyxf('font: height 120; align: wrap on, horiz center')
        base_style_left = xlwt.easyxf('font: height 120; align: wrap on, horiz left')
        base_style_left2 = xlwt.easyxf('font: height 140, bold on, italic on; align: wrap on, horiz left; border: bottom medium;')
        base_style_right = xlwt.easyxf('font: height 120; align: wrap on, horiz right')
        base_style_right2 = xlwt.easyxf('font: height 160, bold on; align: wrap on, horiz right')
        decimal_style = xlwt.easyxf('font: height 140; align: wrap yes, horiz right',num_format_str='$#,##0.00')
        decimal_style2 = xlwt.easyxf('font: height 140, bold on; align: wrap yes, horiz right; border: bottom medium;',num_format_str='$#,##0.00')
        date_style = xlwt.easyxf('font: height 120; align: wrap yes; font: bold on; align: wrap on, horiz center, vert center;', num_format_str='DD-MM-YYYY')
        date_style_title = xlwt.easyxf('font: bold on, height 160; align: wrap yes; font: bold on; align: wrap on, horiz center, vert center;', num_format_str='DD-MM-YYYY')
        datetime_style = xlwt.easyxf('font: height 140; align: wrap yes', num_format_str='YYYY-MM-DD HH:mm:SS')

        if self.report == "monthly":
            periods = period_obj.search([
                                        '&','|','&',
                                        ('fiscalyear_id','=',self.period_id.fiscalyear_id.id),
                                        ('date_stop','<',self.period_id.date_start),
                                        ('date_start','=',self.period_id.date_start),
                                        ('special','=',False)
                                    ])
            for report in report_obj.browse(self.env.cr, self.env.uid, report_ids):
                total_bal01 = total_bal02 = total_bal03 = total_bal04 = total_bal05 = total_bal06 = total_bal07 = total_bal08 = total_bal09 = total_bal10 = total_bal11 = total_bal12 = 0.0
                if report.type == 'accounts' and report.account_ids:
                    account_ids = account_obj._get_children_and_consol(self.env.cr, self.env.uid, [x.id for x in report.account_ids])
                elif report.type == 'account_type' and report.account_type_ids:
                    account_ids = account_obj.search(self.env.cr, self.env.uid, [('user_type','in', [x.id for x in report.account_type_ids])])
                if account_ids:
                    for account in account_obj.browse(self.env.cr, self.env.uid, account_ids):
                        balances = {}
                        for period in periods:
                            self.env.cr.execute(""" select sum(debit), sum(credit) from account_move_line
                                                        where period_id = %s
                                                        and account_id = %s and state = 'valid' """%(period.id, account.id))
                            query = self.env.cr.fetchall()
                            debit = query[0][0] is not None and query[0][0] or 0.0
                            credit = query[0][1] is not None and query[0][1] or 0.0
                            balances.update({period.code:self.get_balance(debit, credit)})
                        if report.display_detail == 'detail_flat' and account.type == 'view':
                            continue
                        if self.is_zero(account, balances):
                            continue
                        vals = {
                            'code': account.code,
                            'name': account.name,
                            'balance01':  balances.get('01/'+year,0.0) and balances['01/'+year] * report.sign or 0.0,
                            'balance02':  balances.get('02/'+year,0.0) and balances['02/'+year] * report.sign or 0.0,
                            'balance03':  balances.get('03/'+year,0.0) and balances['03/'+year] * report.sign or 0.0,
                            'balance04':  balances.get('04/'+year,0.0) and balances['04/'+year] * report.sign or 0.0,
                            'balance05':  balances.get('05/'+year,0.0) and balances['05/'+year] * report.sign or 0.0,
                            'balance06':  balances.get('06/'+year,0.0) and balances['06/'+year] * report.sign or 0.0,
                            'balance07':  balances.get('07/'+year,0.0) and balances['07/'+year] * report.sign or 0.0,
                            'balance08':  balances.get('08/'+year,0.0) and balances['08/'+year] * report.sign or 0.0,
                            'balance09':  balances.get('09/'+year,0.0) and balances['09/'+year] * report.sign or 0.0,
                            'balance10':  balances.get('10/'+year,0.0) and balances['10/'+year] * report.sign or 0.0,
                            'balance11':  balances.get('11/'+year,0.0) and balances['11/'+year] * report.sign or 0.0,
                            'balance12':  balances.get('12/'+year,0.0) and balances['12/'+year] * report.sign or 0.0,
                            'type': 'account',
                            'level': report.display_detail == 'detail_with_hierarchy' and min(account.level + 1,6) or 6, #account.level + 1
                            'account_type': account.type,
                        }
                        #Sumatoria de totales por reporte hijo
                        total_bal01 += vals['balance01']
                        total_bal02 += vals['balance02']
                        total_bal03 += vals['balance03']
                        total_bal04 += vals['balance04']
                        total_bal05 += vals['balance05']
                        total_bal06 += vals['balance06']
                        total_bal07 += vals['balance07']
                        total_bal08 += vals['balance08']
                        total_bal09 += vals['balance09']
                        total_bal10 += vals['balance10']
                        total_bal11 += vals['balance11']
                        total_bal12 += vals['balance12']

                        lines.append(vals)
                #Lineas de consolidados o reportes hijos
                vals = {
                    'code': '',
                    'name': 'TOTAL '+ report.name.upper(),
                    'balance01': total_bal01 * report.sign or 0.0,
                    'balance02': total_bal02 * report.sign or 0.0,
                    'balance03': total_bal03 * report.sign or 0.0,
                    'balance04': total_bal04 * report.sign or 0.0,
                    'balance05': total_bal05 * report.sign or 0.0,
                    'balance06': total_bal06 * report.sign or 0.0,
                    'balance07': total_bal07 * report.sign or 0.0,
                    'balance08': total_bal08 * report.sign or 0.0,
                    'balance09': total_bal09 * report.sign or 0.0,
                    'balance10': total_bal10 * report.sign or 0.0,
                    'balance11': total_bal11 * report.sign or 0.0,
                    'balance12': total_bal12 * report.sign or 0.0,
                    'type': 'report',
                    'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                    'account_type': report.type =='sum' and 'view' or False,
                }
                lines.append(vals)

            #Construimos el xls
            worksheet = workbook.add_sheet(name)
            columns = ['Código','Descripción','ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC']
            worksheet.write_merge(0, 2, 0, 1, '%s\nPeriodo: %s\nFecha: %s'%(company,self.period_id.name,today),header_style1)
            worksheet.write_merge(4, 4, 0, 13, 'Balance de Situacion Mensualizado Hasta %s'%(self.period_id.name.replace('/','-')), header_style2)
            for i, fieldname in enumerate(columns):
                worksheet.write(5, i, fieldname, title_style)
            
            row_index = 6

            for i in lines:
                name_style = i['type'] == 'report' and base_style_left2 or base_style_left
                num_style = i['type'] == 'report' and base_style_left2 or decimal_style
                worksheet.write(row_index, 0, re.sub("\r", " ", str(i['code'])), base_style_right)
                worksheet.write(row_index, 1, re.sub("\r", " ", unicode(i['name']).encode("ascii","ignore")), name_style)
                worksheet.write(row_index, 2, re.sub("\r", " ", str(i['balance01'])), num_style)
                worksheet.write(row_index, 3, re.sub("\r", " ", str(i['balance02'])), num_style)
                worksheet.write(row_index, 4, re.sub("\r", " ", str(i['balance03'])), num_style)
                worksheet.write(row_index, 5, re.sub("\r", " ", str(i['balance04'])), num_style)
                worksheet.write(row_index, 6, re.sub("\r", " ", str(i['balance05'])), num_style)
                worksheet.write(row_index, 7, re.sub("\r", " ", str(i['balance06'])), num_style)
                worksheet.write(row_index, 8, re.sub("\r", " ", str(i['balance07'])), num_style)
                worksheet.write(row_index, 9, re.sub("\r", " ", str(i['balance08'])), num_style)
                worksheet.write(row_index, 10, re.sub("\r", " ", str(i['balance09'])), num_style)
                worksheet.write(row_index, 11, re.sub("\r", " ", str(i['balance10'])), num_style)
                worksheet.write(row_index, 12, re.sub("\r", " ", str(i['balance11'])), num_style)
                worksheet.write(row_index, 13, re.sub("\r", " ", str(i['balance12'])), num_style)
                row_index += 1

            worksheet.col(0).width = 2500
            worksheet.col(1).width = 11000
            worksheet.col(2).width = 2000
            worksheet.col(3).width = 2000
            worksheet.col(4).width = 2000
            worksheet.col(5).width = 2000
            worksheet.col(6).width = 2000
            worksheet.col(7).width = 2000
            worksheet.col(8).width = 2000
            worksheet.col(9).width = 2000
            worksheet.col(10).width = 2000
            worksheet.col(11).width = 2000
            worksheet.col(12).width = 2000
            worksheet.col(13).width = 2000
        if self.report == "standar":
            date_start = datetime.strptime(self.period_id.date_start,'%Y-%m-%d')
            year_stop = datetime.strptime(self.period_id.fiscalyear_id.date_stop,'%Y-%m-%d')
            last_year_stop = '%s-%s-%s'%(str(year_stop.year - 1), str(year_stop.month).zfill(2), str(year_stop.day).zfill(2))
            last_period = False
            fyear_last_period = False
            for p in period_obj.search([('special','=',False)]):
                if datetime.strptime(p.date_stop,'%Y-%m-%d') == (date_start - timedelta(days=1)):
                    last_period = p
                if p.date_stop == last_year_stop:
                    fyear_last_period = p
            for report in report_obj.browse(self.env.cr, self.env.uid, report_ids):
                total_period = total_last_period = total_last_year = total_var = 0.0
                if report.type == 'accounts' and report.account_ids:
                    account_ids = account_obj._get_children_and_consol(self.env.cr, self.env.uid, [x.id for x in report.account_ids])
                elif report.type == 'account_type' and report.account_type_ids:
                    account_ids = account_obj.search(self.env.cr, self.env.uid, [('user_type','in', [x.id for x in report.account_type_ids])])
                if account_ids:
                    for account in account_obj.browse(self.env.cr, self.env.uid, account_ids):
                        balances = {}
                        for period in [self.period_id,last_period,fyear_last_period]:
                            if period:
                                self.env.cr.execute(""" select sum(debit), sum(credit) from account_move_line
                                                            where period_id = %s
                                                            and account_id = %s and state = 'valid' """%(period.id, account.id))
                                query = self.env.cr.fetchall()
                                debit = query[0][0] is not None and query[0][0] or 0.0
                                credit = query[0][1] is not None and query[0][1] or 0.0
                                balances.update({period.code:self.get_balance(debit, credit)})
                        if report.display_detail == 'detail_flat' and account.type == 'view':
                            continue
                        if self.is_zero(account, balances):
                            continue
                        vals = {
                            'code': account.code,
                            'name': account.name,
                            'balance01':  balances.get(self.period_id.code,0.0) and balances[self.period_id.code] * report.sign or 0.0,
                            'balance02':  balances.get(last_period and last_period.code or '',0.0) and balances[last_period.code] * report.sign or 0.0,
                            'balance03':  balances.get(fyear_last_period and fyear_last_period.code or '',0.0) and balances[fyear_last_period.code] * report.sign or 0.0,
                            'type': 'account',
                            'level': report.display_detail == 'detail_with_hierarchy' and min(account.level + 1,6) or 6, #account.level + 1
                            'account_type': account.type,
                        }
                        #Sumatoria de totales por reporte hijo
                        total_period += vals['balance01']
                        total_last_period += vals['balance02']
                        total_last_year += vals['balance03']

                        lines.append(vals)
                #Lineas de consolidados o reportes hijos
                vals = {
                    'code': '',
                    'name': 'TOTAL '+ report.name.upper(),
                    'balance01': total_period * report.sign or 0.0,
                    'balance02': total_last_period * report.sign or 0.0,
                    'balance03': total_last_year * report.sign or 0.0,
                    'type': 'report',
                    'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                    'account_type': report.type =='sum' and 'view' or False,
                }
                lines.append(vals)
            
            worksheet = workbook.add_sheet(name)

            columns = ['Código','Descripción',self.period_id.name,last_period and last_period.name or '',fyear_last_period and fyear_last_period.name or '','Varia.','Obs']
            worksheet.write_merge(0, 2, 0, 1, '%s\nPeriodo: %s\nFecha: %s'%(company,self.period_id.name,today),header_style1)
            worksheet.write_merge(4, 4, 0, 6, 'Analisis Evolucion Balance de Situacion al %s'%(self.period_id.name.replace('/','-')), header_style2)
            for i, fieldname in enumerate(columns):
                worksheet.write(5, i, fieldname, title_style)
            
            row_index = 6
            for i in lines:
                name_style = i['type'] == 'report' and base_style_left2 or base_style_left
                num_style = i['type'] == 'report' and base_style_left2 or decimal_style
                var = i['balance01'] - i['balance03']
                worksheet.write(row_index, 0, re.sub("\r", " ", str(i['code'])), base_style_right)
                worksheet.write(row_index, 1, re.sub("\r", " ", unicode(i['name']).encode("ascii","ignore")), name_style)
                worksheet.write(row_index, 2, re.sub("\r", " ", str(i['balance01'])), num_style)
                worksheet.write(row_index, 3, re.sub("\r", " ", str(i['balance02'])), num_style)
                worksheet.write(row_index, 4, re.sub("\r", " ", str(i['balance03'])), num_style)
                worksheet.write(row_index, 5, re.sub("\r", " ", str(var)), num_style)
                worksheet.write(row_index, 6, re.sub("\r", " ", ''), num_style)
                total_var += var
                row_index += 1

            worksheet.col(0).width = 2500
            worksheet.col(1).width = 11000
            worksheet.col(2).width = 2000
            worksheet.col(3).width = 2000
            worksheet.col(4).width = 2000
            worksheet.col(5).width = 2000
            worksheet.col(6).width = 8000

        #Descargamos el xls en el cliente
        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        data_b64 = base64.encodestring(data)
        attach_vals = {
                 'name': '%s - %s.xls'%(name, today),
                 'datas':data_b64,
                 'datas_fname': '%s - %s.xls'%(name, today),
                 }
        doc = self.env['ir.attachment'].create(attach_vals)
        
        return {
                    'type' : 'ir.actions.act_url',
                    'url':   '/web/binary/saveas?model=ir.attachment&field=datas&filename_field=name&id=%s' % (doc.id),
                    'target': 'self',
                }

    @api.model
    def _default_period(self):
        user_obj = self.env['res.users']
        company = user_obj.browse(self.env.uid).company_id
        period_obj = self.env['account.period']
        today = date.today().strftime(DATE_FORMAT)
        period = period_obj.search(
            [('date_start', '<=', today),
             ('date_stop', '>=', today),
             ('company_id', '=', company.id)])
        if period:
            return period.id
            
    @api.model
    def _default_report(self):
        report = self.env.ref('account.account_financial_report_balancesheet0')
        if report:
            return report.id

    financial_report_id = fields.Many2one('account.financial.report', string="Reporte Financiero", help="Seleccione el reporte financiero", default=_default_report)
    period_id = fields.Many2one('account.period', string="Periodo", help="Período contable", default=_default_period)
    report = fields.Selection([('standar','Estándar'),('monthly','Mensualizado')], string="Reporte", default="standar",help="Seleccione el tipo de informe que desea generar")
