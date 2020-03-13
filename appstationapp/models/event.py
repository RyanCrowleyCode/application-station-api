from django.db import models
from .job import Job

class Event(models.Model):
    """
    This class is responsible for creating the Event instances.

    Author: 
        Ryan Crowley
    """

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    details = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    class Meta:
        ordering = ("start_time", ) 
        verbose_name = ("event")
        verbose_name_plural = ("events")

    def __str__(self):
        return f'{self.details} beginning {self.start_time} and ending {self.end_time} (for application {self.application}'

    


