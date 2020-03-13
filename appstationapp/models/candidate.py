from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    """
    This class is responsible for creating the Candidate instances.
    Candidates are users.

    Author: 
        Ryan Crowley
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("candidate")
        verbose_name_plural = ("candidates")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

