from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta
from odoo.tools import float_compare




class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The offer price must be strictly positive"),
    ]    


    price = fields.Float('Price', required=True)
    status = fields.Selection([('accepted','Accepted') ,('refused','Refused')],string="Status",copy=False,default = False)
    partner_id = fields.Many2one("res.partner",string="Partner",required = True)
    property_id = fields.Many2one("estate.property",string="Property",required = True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)
    validity = fields.Integer("Validity(days)",default=7)
    date_deadline = fields.Date(string="Deadline",compute="_compute_date_deadline_",inverse="_inverse_date_deadline_")


    @api.depends("create_date", "validity")
    def _compute_date_deadline_(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline_(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    

    def action_accept(self):
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("Cannot accept offer for a sold property.")
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
        
    