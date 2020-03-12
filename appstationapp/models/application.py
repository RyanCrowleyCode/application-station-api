from django.db import models
from djrichtextfield.widgets import RichTextField
from django.contrib.auth.models import User
from .status import Status
from .job import Job

class Application(models.Model):
    """
    This class is responsible for creating the Application instances.

    Author: 
        Ryan Crowley
    """

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)


    class Meta:
        verbose_name = ("application")
        verbose_name_plural = ("applications")

    def __str__(self):
        return f'Application # {self.id}: {self.job.title} ({self.job.company.name})'

    


