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


class District(models.Model):
    _name = 'hirms.district'
    _description = 'administrative districts'

    name = fields.Char(
        string="District",
        required=True,
    )
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text('Note')

    _sql_constraints = [
        (
            'name_country_uniq',
            'unique(name,country_id)',
            'District name must be unique for this country!'
        ),
    ]

