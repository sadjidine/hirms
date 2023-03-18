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
from odoo.tools.populate import compute
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta


class Insured(models.Model):
    _name = 'hirms.insured'
    _description = 'insured patients'
    _inherits = {'res.partner': "partner_id"}

    partner_id = fields.Many2one('res.partner', ondelete='cascade', required=True)
    policy_id = fields.Many2one(
        comodel_name='hirms.policy',
        string='Policy',
        required=True
    )
    firstname = fields.Char(string="First Name", size=128, required=True)
    lastname = fields.Char(string="Last Name", size=32, required=True)
    fullname = fields.Char(string="Name", compute="_get_full_name")
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        required=True,
    )
    date_birth = fields.Date(string='Date of Birth', required=True)
    date_decease = fields.Date(string='Date of decease', compute="_get_decease_date", store=True)
    date_registration = fields.Date(string='Date of registration', default=fields.Date.today())
    date_activation = fields.Date(string='Date of Activation', help='Date of reactivation')
    date_reactivation = fields.Date(string='Date of reactivation', help='Date of reactivation')
    administrative_ref = fields.Char(required=False)
    profession = fields.Char(string="Profession", help="Insured Occupation")
    id_code = fields.Char(
        string='Id. code',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        compute="_get_id_code",
        help="The system provides an incremental identification code for every created insured."
    )
    external_id = fields.Char(
        string='External Id.',
        required=False
    )
    api_external_id = fields.Char(
        string='API External Id.',
        required=False
    )

    family_status = fields.Selection(
        [
            ('member', 'Member'),
            ('conjunct', 'Conjunct'),
            ('child', 'Child'),
            ('other', 'Other')
        ],
        default="member",
        compute="_get_family_status",
        store=True,
    )
    relationship = fields.Selection(
        [
            ('conjunct', 'Conjunct'),
            ('child', 'Child'),
            ('other', 'Other')
        ],
        help="Select the corresponding status of insured in the family..."
    )
    locality_id = fields.Many2one(
        comodel_name='hirms.locality',
        string='Locality',
        required=False,
    )
    organization_id = fields.Many2one(
        comodel_name='hirms.organization',
        string='Organization unit',
        required=False
    )
    insured_seq = fields.Char(
        string='Insured Num.',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    # subscription_id = fields.Many2one(
    #     string='Member\'s Subscription',
    #     comodel_name='hirms.subscription',
    #     ondelete='restrict',
    #     index=True,
    # )
    member_id = fields.Many2one(
        comodel_name='hirms.insured',
        string='Member',
        ondelete='restrict',
        index=True,
        required=False
    )
    family_ids = fields.One2many(
        comodel_name='hirms.insured',
        inverse_name='member_id',
        string='Assigns',
        help="Assigns depending on member!"
    )
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    age_details = fields.Char(compute='_compute_age_details')
    weight = fields.Integer('Insured weight', help="The weight in Kilogram (kg)")
    height = fields.Integer('Insured height', help="The whight (in cemtimeter (cm)")
    bmi = fields.Float(
        string="BMI",
        digits=(4, 2),
        compute='_compute_bmi',
        help="Calculate the Body Mass Index"
    )
    blood_group = fields.Many2one('hirms.blood', string="Blood Group")
    risk_id = fields.Many2one('hirms.genetic.risks', "Genetic Risks")
    active = fields.Boolean(
        default=True,
    )
    note = fields.Html('Note', sanitize_style=True)

    def name_get(self):
        res = []
        for rec in self:
            rec_name = rec.name.strip()
            res.append((rec.id, "%s (%s)" % (rec_name, rec.id_code)))
        return res

    @api.onchange('firstname', 'lastname')
    def _get_full_name(self):
        firstname = None
        lastname = None
        if self.firstname:
            firstname = self.firstname.lstrip().rstrip()
        if self.lastname:
            lastname = self.lastname.strip()
        self.name = "%s %s" % (lastname, firstname)
        self.fullname = self.name

    def _get_id_code(self):
        self.ensure_one()
        if not self.id_code and self.name:
            name = self.name.strip()
            name_tab = name.split(' ')
            sequence = self.insured_seq[4:]
            if len(name_tab) > 1:
                self.id_code = sequence + name_tab[0][0] + name_tab[1][0]

    @api.depends('relationship')
    def _get_family_status(self):
        """
        Get family status
        """
        for rec in self:
            if rec.relationship == 'conjunct':
                rec.family_status = 'conjunct'
            elif rec.relationship == 'child':
                rec.family_status = 'child'
            elif rec.relationship == 'other':
                rec.family_status = 'other'
            else:
                rec.family_status = 'member'

    def _get_decease_date(self):
        for rec in self:
            insured = self.env['hirms.decease'].search([
                ('insured_id', '=', rec.id)
            ])
            if insured:
                rec.date_decease = insured.date_decease

    @api.depends('date_birth')
    def _compute_age(self):
        """
        Age calculation of insured
        """
        for rec in self:
            rec.age = 0
            if rec.date_birth:
                age = int((date.today() - rec.date_birth) // timedelta(days=365.2425))
                rec.age = age

    @api.depends('date_birth')
    def _compute_age_details(self):
        """
        Details Age calculation of insured
        """
        now = datetime.now()
        for rec in self:
            dob = fields.Datetime.from_string(rec.date_birth)
            # deceased = True if rec.date_decease else False
            if bool(rec.date_decease):
                dod = fields.Datetime.from_string(rec.date_decease)
                delta = relativedelta(dod, dob)
                text = _('(deceased)')
            else:
                delta = relativedelta(now, dob)
                text = ''
            years = '%s' % delta.years
            years_month_days = '%s %s-%s %s-%s %s %s' % (
                delta.years, _('years'),
                delta.months, _('months'),
                delta.days, _('days'),
                text
            )
            rec.age_details = years_month_days

    @api.depends('weight', 'height')
    def _compute_bmi(self):
        """
        BMI calculation
        """
        for rec in self:
            if rec.weight and rec.height:
                rec.bmi = (rec.weight / ((rec.height/100)**2))

    @api.model
    def create(self, vals):
        if vals.get('insured_seq', _('New')) == _('New'):
            vals['insured_seq'] = self.env['ir.sequence'].next_by_code(
                'hirms.insured') or _('New')
        result = super(Insured, self).create(vals)
        return result


