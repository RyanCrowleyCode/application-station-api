from django.db import models

class Job(models.Model):
    """
    This class is responsible for creating the Job instances.

    Author: 
        Ryan Crowley
    """

    title = models.CharField(max_length=100)

    class Meta:
        ordering = ("company_id", )
        verbose_name = ("job")
        verbose_name_plural = ("jobs")

    def __str__(self):
        return self.name

    


