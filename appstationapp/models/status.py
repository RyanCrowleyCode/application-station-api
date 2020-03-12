from django.db import models

class Status(models.Model):
    """
    This class is responsible for creating the Status instances.

    Author: 
        Ryan Crowley
    """

    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("status")
        verbose_name_plural = ("statuses")

    def __str__(self):
        return self.status

    


