from datetime import date, timedelta

from odoo import models, fields, api

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        copy=False
    )

    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    validity = fields.Integer(string="Validity", default=7)

    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True
    )
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date_as_date = record.create_date.date()
                delta = (record.date_deadline - create_date_as_date).days
                record.validity = delta
            elif record.date_deadline:
                record.validity = 0

    def action_edit_property_tag(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': self.env.context
        }