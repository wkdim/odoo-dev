from odoo import models,fields,api


class Stages(models.Model):
    _inherit = 'hr.recruitment.stage'


    interview_stages= fields.Boolean("Show Interview Questions")
    

    

