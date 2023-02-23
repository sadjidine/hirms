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


class Policy(models.Model):
    _name = 'hirms.policy'
    _description = 'insurance policies'

    name = fields.Char(
        string="Policy",
        required=True,
    )
    code = fields.Char(
        size=32,
        required=False,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Organisation",
        required=True,
    )
    gender_control = fields.Boolean(
        default=False,
        help="Checked to allow the system to check the gender for assigns declaration...",
    )
    suspending_period = fields.Integer(
        # Delai de carence
        default=0,
        help="Define the waiting period (in days)...",
    )
    individual_limit = fields.Float(
        digits=(9, 0),
        help="Indicate the individual ceiling amount...",
    )
    family_limit = fields.Float(
        digits=(9, 0),
        help="Indicate the family ceiling amount...",
    )
    public_coverage_rate = fields.Integer(
        default=0,
        help="Define the public coverage rate (in percentage)...",
    )
    private_coverage_rate = fields.Integer(
        default=0,
        help="Define the private coverage rate (in percentage)...",
    )
    public_coverage_refund_rate = fields.Integer(
        string=" Public Refund Rate",
        default=0,
        help="Define the public coverage rate for refund (in percentage)...",
    )
    private_coverage_refund_rate = fields.Integer(
        string=" Private Refund Rate",
        default=0,
        help="Define the private coverage rate for refund (in percentage)...",
    )
    refund_validity = fields.Integer(
        default=0,
        help="Define the refund validity (in days)...",
    )
    maxi_refund_number = fields.Integer(
        default=0,
        help="Define the maximum refund number allowed per member/exercise...",
    )
    refund_limit = fields.Float(
        digits=(6, 0),
        help="Indicate the amount limit per refund...",
    )
    individual_refund_limit = fields.Float(
        digits=(6, 0),
        help="Indicate the individual refund amount limit...",
    )
    family_refund_limit = fields.Float(
        digits=(6, 0),
        help="Indicate the family refund amount limit...",
    )
    maxi_member_age = fields.Integer(
        default=0,
        help="Define the maximum age (years) for someone to subscribe a membership...",
    )
    maxi_spouse_age = fields.Integer(
        default=0,
        help="Define the maximum age (years) for someone to enroll as spouse declared by a member...",
    )
    maxi_child_age = fields.Integer(
        default=0,
        help="Define the maximum age (years) for someone to subscribe as child declared by a member...",
    )
    maxi_filiation_age = fields.Integer(
        default=0,
        help="Define the maximum age (years) for someone to subscribe as other parent declared by a member...",
    )
    children_limit = fields.Integer(
        string="Limit number of children",
        default=0,
        help="Define the number of limit allowed for declared children ...",
    )
    children_add_allowed = fields.Integer(
        default=0,
        help="Define the number of additional children allowed...",
    )
    child_age_majority = fields.Integer(
        default=0,
        help="Define qge of majority for children allowed...",
    )
    spouse_limit = fields.Integer(
        string="Limit number of children",
        default=0,
        help="Define the number of limit allowed for declared spouse ...",
    )
    spouse_add_allowed = fields.Integer(
        default=0,
        help="Define the number of additional spouse(s) allowed...",
    )
    filiation_limit = fields.Integer(
        string="Limit number of children",
        default=0,
        help="Define the number of limit allowed for declared filiation ...",
    )
    filiation_add_allowed = fields.Integer(
        default=0,
        help="Define the number of additional filiation(s) allowed...",
    )
    medication_maxi_line = fields.Integer(
        default=0,
        help="Define the maximum number of medication lines allowed per care process...",
    )
    medication_limit = fields.Float(
        digits=(6, 0),
        help="Indicate medication maximum amount allowed per care process...",
    )
    medication_product_limit = fields.Float(
        digits=(6, 0),
        help="Indicate the maximum allowed price for pharmaceutical product...",
    )
    childbirth_donation = fields.Float(
        digits=(6, 0),
        help="Indicate the amount allowed for every childbirth in public hospital...",
    )
    alert_threshold = fields.Integer(
        default=0,
        help="Define the level (in percentage) of throwing alert message in the system...",
    )
    medical_care_validity = fields.Integer(
        string="Process validity",
        default=0,
        help='Define the medical care process validity (in hours)'
    )
    product_margin = fields.Float(
        digits=(6, 0),
        default=0,
        help="Set the tolerated margin of the pharmaceutical product price"
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note & description",
        required=False,
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'Category name must be unique'
        ),
        (
            'code_uniq',
            'unique(code)',
            'Category name must be unique'
        ),
    ]


class CodificationControl(models.Model):
    _name = 'hirms.code.control'
    _description = 'policy medical code control'

    codification_id = fields.Many2one(
        comodel_name="hirms.codification",
        string="Medical Code",
        ondelete="restrict",
        required=True,
    )
    policy_id = fields.Many2one(
        comodel_name="hirms.policy",
        string="Insurance Policy",
        ondelete="restrict",
        required=True,
    )
    public_cover_rate = fields.Integer(
        string="Public Rate (%)",
        Default=0,
    )
    private_cover_rate = fields.Integer(
        string="Private Rate (%)",
        Default=0,
    )
    refund_cover_rate = fields.Integer(
        string="Refund Cover Rate (%)",
        Default=0,
    )
    individual_limit = fields.Float(
        string="Limit/individual",
        digits=(7, 0),
    )
    family_limit = fields.Float(
        string="Limit/family",
        digits=(7, 0),
    )
    pending_period = fields.Integer(
        default=0,
        help="Set the waiting period (timeout) in days, between 2 procedures for this medical code!"
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note & description",
        required=False,
    )

    _sql_constraints = [
        (
            'codification_policy_uniq',
            'unique(codification_id, policy_id)',
            'Medical code related to policy must be unique'
        )
    ]


class CategoryControl(models.Model):
    _name = 'hirms.category.control'
    _description = 'policy category control'

    category_id = fields.Many2one(
        comodel_name="hirms.category",
        string="Medical Category",
        ondelete="restrict",
        required=True,
    )
    policy_id = fields.Many2one(
        comodel_name="hirms.policy",
        string="Insurance Policy",
        ondelete="restrict",
        required=True,
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('all', 'All'),
        ],
        default='all',
        required=True,
        help='Select the gender which aims by this control'
    )
    family_status = fields.Selection(
        selection=[
            ('member', 'Member'),
            ('spouse', 'Spouse'),
            ('child', 'Child'),
            ('member_spouse', 'Member + Spouse'),
            ('member_child', 'Member + Child'),
            ('spouse_child', 'Spouse + Child'),
            ('all', 'All'),
        ],
        default='all',
        required=True,
        help='Select the family status which aims by this control'
    )
    individual_process_limit = fields.Integer(
        string="Process limit/individual",
        Default=0,
    )
    family_process_limit = fields.Integer(
        string="Process limit/family",
        Default=0,
    )
    individual_amount_limit = fields.Float(
        string="Amount limit/individual",
        digits=(9, 0),
        Default=0,
    )
    family_amount_limit = fields.Float(
        string="Amount limit/family",
        digits=(9, 0),
        Default=0,
    )
    private_cover_rate = fields.Integer(
        string="Private Rate (%)",
        Default=0,
    )
    refund_cover_rate = fields.Integer(
        string="Refund Cover Rate (%)",
        Default=0,
    )
    individual_limit = fields.Float(
        string="Limit/individual",
        digits=(7, 0),
    )
    family_limit = fields.Float(
        string="Limit/family",
        digits=(7, 0),
    )
    suspending_period = fields.Integer(
        default=0,
        help="Set the suspending period (timeout) in days!"
    )
    pending_period = fields.Integer(
        default=0,
        help="Set the waiting period (timeout) in days, between 2 procedures for this control!"
    )
    minimum_age = fields.Integer(
        default=0,
        help="Set the minimum patient age required for this control!"
    )
    maximum_age = fields.Integer(
        default=0,
        help="Set the maximum patient age required for this control!"
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note & description",
        required=False,
    )

    _sql_constraints = [
        (
            'category_policy_uniq',
            'unique(category_id, policy_id)',
            'Category related to policy must be unique'
        )
    ]