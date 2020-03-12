from django.db import models
from djrichtextfield.widgets import RichTextField
from django.contrib.auth.models import User
from .question import Question

class UserQuestion(models.Model):
    """
    This class is responsible for creating the UserQuestion instances.

    Author: 
        Ryan Crowley
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    answer = RichTextField()


    class Meta:
        verbose_name = ("userquestion")
        verbose_name_plural = ("userquestions")



    


