from django.db import models

class Company(models.Model):
    """
    This class is responsible for creating the Company instances.

    Author: 
        Ryan Crowley
    """

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name", )
        verbose_name = ("company")
        verbose_name_plural = ("companies")

    def __str__(self):
        return self.name

    


