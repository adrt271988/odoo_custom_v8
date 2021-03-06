# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
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
###############################################################################

from openerp import models, fields, api


class OpAllStudentWizard(models.TransientModel):
    _name = 'op.all.student'

    course_id = fields.Many2one(
        'op.course', 'Course',
        default=lambda self: self.env['op.attendance.sheet'].browse(
            self.env.context['active_id']).register_id.course_id.id or False,
        readonly=True)
    standard_id = fields.Many2one(
        'op.standard', 'Standard',
        default=lambda self: self.env['op.attendance.sheet'].browse(
            self.env.context['active_id']).register_id.standard_id.id or False,
        readonly=True)
    batch_id = fields.Many2one(
        'op.batch', 'Batch',
        default=lambda self: self.env['op.attendance.sheet'].browse(
            self.env.context['active_id']).register_id.batch_id.id or False,
        readonly=True)
    division_id = fields.Many2one(
        'op.division', 'Division',
        default=lambda self: self.env['op.attendance.sheet'].browse(
            self.env.context['active_id']).register_id.division_id.id or False,
        readonly=True)
    student_ids = fields.Many2many('op.student', string='Add Student(s)')

    @api.one
    def confirm_student(self):
        data = self.read()[0]
        data.update(
            {'ids': self.env.context.get('active_ids', []),
             'student_ids': data['student_ids']})
        for sheet in self.env.context.get('active_ids', []):
            sheet_browse = self.env['op.attendance.sheet'].browse(sheet)
            absent_list = [
                x.student_id.id for x in sheet_browse.attendance_line]
            all_student_search = self.env['op.student'].search(
                [('course_id', '=', sheet_browse.register_id.course_id.id),
                 ('standard_id', '=', sheet_browse.register_id.standard_id.id),
                 ('division_id', '=', sheet_browse.register_id.division_id.id),
                 '|',
                 ('course_id', '=', sheet_browse.register_id.course_id.id),
                 ('standard_id', '=', sheet_browse.register_id.standard_id.id)]
            )
            all_student_search = list(
                set(all_student_search) - set(absent_list))
            for student_data in all_student_search:
                if student_data.id in data['student_ids']:
                    self.env['op.attendance.line'].create(
                        {'student_id': student_data.id, 'absent': False,
                         'attendance_id': self.env.context.get('active_id')})
                else:
                    self.env['op.attendance.line'].create(
                        {'student_id': student_data.id, 'present': True,
                         'attendance_id': self.env.context.get('active_id')})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
