from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Tag of property"

    name = fields.Char(string='Name', required=True)

    def action_edit_property_tag(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
            'context': self.env.context
        }