from odoo import fields, models, api

class ApplicantQuestionRating(models.Model):
    _name = 'hr.applicant.question.rating'
    _description = 'Applicant Question Rating'

    applicant_id = fields.Many2one(
        'hr.applicant',
        string="Applicant",
        required=True,
        ondelete='cascade'
    )
    
    question_id = fields.Many2one(
        'hr.job.question',
        string="Question",
        required=True,
        ondelete='cascade'
    )
    
    question_title = fields.Char(
        related='question_id.title',
        string="Question Title",
        readonly=True,
        store=True
    )
    
    rating = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ], string="Rating")
    
    comment = fields.Text("Comment")

class Applicant(models.Model):
    _inherit = 'hr.applicant'

    question_ratings = fields.One2many(
        'hr.applicant.question.rating',
        'applicant_id',
        string="Question Ratings",
        ondelete='cascade'
    )
    
    interview_score = fields.Float(
        string="Interview Score",
        store=True
    )
    
    is_interview_stage = fields.Boolean(
        string="Is Interview Stage",
        compute='_compute_is_interview_stage',
        store=True
    )

    @api.depends('stage_id', 'stage_id.interview_stages')
    def _compute_is_interview_stage(self):
        for applicant in self:
            applicant.is_interview_stage = applicant.stage_id.interview_stages if applicant.stage_id else False

    @api.model
    def create(self, vals):
        new_applicant = super(Applicant, self).create(vals)
        new_applicant.create_question_ratings()
        return new_applicant

    def write(self, vals):
        result = super(Applicant, self).write(vals)
        if 'stage_id' in vals:
            self.create_question_ratings()
        return result

    def create_question_ratings(self):
        for applicant in self:
            if not applicant.is_interview_stage or not applicant.job_id:
                continue

        job_questions = applicant.job_id.question_ids
        existing_ratings = applicant.question_ratings

        ratings_to_remove = []
        for rating in existing_ratings:
            if rating.question_id not in job_questions:
                ratings_to_remove.append(rating)
        
        for rating in ratings_to_remove:
            rating.unlink()

        existing_question_ids = []

        for rating in existing_ratings:
            existing_question_ids.append(rating.question_id.id)
            
        for question in job_questions:
            if question.id not in existing_question_ids:
                self.env['hr.applicant.question.rating'].create({
                    'applicant_id': applicant.id,
                    'question_id': question.id,
                })


    def calculate_performance(self):
        for applicant in self:
            ratings = []

        for rating in applicant.question_ratings:
              if rating.rating:
                ratings.append(float(rating.rating))  
                     
              if ratings:
                total_ratings = sum(ratings)
                max_possible_score = len(ratings) * 5
                applicant.interview_score = (total_ratings / max_possible_score) * 100
              else:
                applicant.interview_score = 0
