# -*- coding: utf-8 -*-
from odoo import fields, models, api

class Question(models.Model):
    _name = 'hr.job.question'
    _description = 'Job Position Question'
    _order = "sequence, title"


    title = fields.Char(string="Questions", required=True)
    job_id = fields.Many2one('hr.job', string="Job Position", ondelete='cascade')
    sequence = fields.Integer('Sequence')

    @api.model
    def create(self, vals):
        new_question = super(Question, self).create(vals)
        
        if new_question.job_id:
            self.update_job_applicants(new_question.job_id)
        
        return new_question

    def unlink(self):
        affected_jobs = []
        for question in self:
            if question.job_id:
                affected_jobs.append(question.job_id)
        
        result = super(Question, self).unlink()
        for job in affected_jobs:
            self.update_job_applicants(job)
            
        return result

    def update_job_applicants(self, job):
        applicants = self.env['hr.applicant'].search([
            ('job_id', '=', job.id),
            ('active', 'in', [True, False])
        ])
        
        for applicant in applicants:
            applicant.create_question_ratings()

class Job(models.Model):
    _inherit = 'hr.job'

    question_ids = fields.One2many(
        'hr.job.question',
        'job_id',
        string="Questions"
    )

  