from django.db import models

# Create your models here.
class Stationary(models.Model):
    styling = models.TextField(verbose_name = "CSS Styling")
