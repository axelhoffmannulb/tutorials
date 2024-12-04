from datetime import date, timedelta
from odoo import models, fields, api

class Property(models.Model):
    _name = "estate.property"
    _description = "Properties of estate"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, store=True)
    bedrooms = fields.Integer(default=3)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        default='north'
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        default='new',
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    partner_id = fields.Many2one("res.partner", string="Buyer")

    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers"
    )

    total_area = fields.Float(compute='_compute_total_area', readonly=True)

    best_price = fields.Float(compute='_compute_best_price', readonly=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'north'
            self.garden_area = 10

    def action_edit_property(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': self.env.context
        }
