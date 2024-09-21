from odoo import fields, models,api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The property type name must be unique"),
    ]


    name = fields.Char('Property Type', required = True)
    sequence = fields.Integer('Sequence')
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.Many2many("estate.property.offer", string="Offers", compute="_compute_offer_")
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_")

    @api.depends("offer_ids")
    def _compute_offer_(self):
        for record in self:
            record.offer_count = len(record.offer_ids)