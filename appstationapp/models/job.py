from django.db import models
from django.contrib.auth.models import User
from .company import Company
from .status import Status
# from djrichtextfield.widgets import RichTextField

class Job(models.Model):
    """
    This class is responsible for creating the Job instances.

    Author: 
        Ryan Crowley
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    class Meta:
        ordering = ("company_id", )
        verbose_name = ("job")
        verbose_name_plural = ("jobs")

    def __str__(self):
        return f'{self.title} ({company.name})'

    


