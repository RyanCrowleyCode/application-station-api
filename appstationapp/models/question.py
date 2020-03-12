from django.db import models

class Question(models.Model):
    """
    This class is responsible for creating the Question instances.

    Author: 
        Ryan Crowley
    """

    question = models.TextField
    is_from_interviewer = models.BooleanField()


    class Meta:
        ordering = ("start_time", ) 
        verbose_name = ("question")
        verbose_name_plural = ("questions")

    def __str__(self):
        return f'"{self.question}" -from interviewer = {self.is_from_interviewer}"'

    


