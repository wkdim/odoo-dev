from odoo import fields, models,api
from dateutil.relativedelta import relativedelta
from odoo.fields import Date
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare,float_is_zero



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Management"
    _order = "id desc"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ] 


    name = fields.Char('Title',required=True)
    description =fields.Text('Description')
    postcode = fields.Char('Post Code')
    date_availability = fields.Date('Date', copy= False, default=Date.today() + relativedelta(days=90))
    expected_price = fields.Float('Expected Price',required= True)
    selling_price = fields.Float('Selling Price',readonly=True, copy= False)
    bedrooms = fields.Integer('Bedrooms',default=2)
    living_area= fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)') 
    garden_orientation = fields.Selection(
    selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    string="Garden Orientation")
    active = fields.Boolean('Active',default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        string='State',
        required=True,
        default='new',
        copy=False   
    )
    property_type_id= fields.Many2one(comodel_name="estate.property.type", string = "Property Type")
    salesperson_id = fields.Many2one(comodel_name="res.users",string="Salesman",default=lambda self: self.env.user)
    buyer_id = fields.Many2one(comodel_name="res.partner",string="Buyer",copy=False)
    tag_ids = fields.Many2many(comodel_name="estate.property.tag",string="Tags")
    offer_ids=fields.One2many("estate.property.offer","property_id",string="Offers")
    total_area = fields.Integer(string='Total Area (sqm)', store=True,compute="_compute_total")
    best_price = fields.Float(string='Best Offer',store=True,compute="_compute_best_offer_")
    

    @api.depends('living_area','garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area= record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_offer_(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange('garden') 
    def _onchange_garden_(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False      

  
   
    def unlink(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise UserError("You cannot delete a property except it is 'New' or 'Canceled' state.")
        return super(EstateProperty, self).unlink()

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled property cannot be sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be canceled.")
            record.state = "canceled"
        return True


         


    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        precision = 2
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=precision):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=precision) < 0:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

                