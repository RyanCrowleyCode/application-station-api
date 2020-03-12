from django.db import models
from djrichtextfield.widgets import RichTextField
from .company import Company

class Job(models.Model):
    """
    This class is responsible for creating the Job instances.

    Author: 
        Ryan Crowley
    """

    title = models.CharField(max_length=100)
    description = RichTextField(max_length=255)
    link = models.CharField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    class Meta:
        ordering = ("company_id", )
        verbose_name = ("job")
        verbose_name_plural = ("jobs")

    def __str__(self):
        return f'{self.title} ({company.name})'

    


