from django.db import models
from .candidate import Candidate
# from djrichtextfield.widgets import RichTextField

class Question(models.Model):
    """
    This class is responsible for creating the Question instances.

    Author: 
        Ryan Crowley
    """

    question = models.TextField()
    is_from_interviewer = models.BooleanField()
    answer = models.TextField(null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("question")
        verbose_name_plural = ("questions")
        

    def __str__(self):
        author = 'Interviewer' if self.is_from_interviewer else 'Me'
        return f'"{self.question}" - {author}'

    


