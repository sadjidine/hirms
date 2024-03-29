# -*- coding: utf-8 -*-
#############################################################################
#
#    SIGEM (Société Ivoirienne d'Expertise, de Gestion et de Management.
#
#    Copyright (C) 2022-TODAY SIGEM(<https://www.sigem.pro>)
#    Author: Salifou OMBOTIMBE(<https://www.linkedin.com/in/ombotimbe-salifou-860a8044>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api


class Pathology(models.Model):
    _name = 'hirms.pathology'
    _description = 'medical pathologies'
    _rec_name = 'code'

    name = fields.Char(
        string="Pathology",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    speciality_id = fields.Many2one(
        comodel_name="hirms.specialization",
        string="Related Specialization",
        ondelete="restrict",
        required=True,
    )
    chronic = fields.Boolean(
        string="Chronic?",
        help="Check to set this pathology as chronic!"
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text('Note')

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'Pathology Code must be unique'
        ),
        (
            'code_uniq',
            'unique(code)',
            'Pathology Name must be unique'
        ),
    ]

