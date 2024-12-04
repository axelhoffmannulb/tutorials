from odoo import models, fields

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Type of property"
    _order = "name"

    name = fields.Char(string='Name', required=True)

    property_ids = fields.One2many('estate.property',"property_type_id", string="Property")

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'Name must be unique')
    ]

    def action_edit_property_type(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': self.env.context
        }