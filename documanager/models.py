from django.db import models

# Create your models here.
class Stationary(models.Model):
    name = models.CharField(max_length=20)
    styling = models.TextField(verbose_name = "CSS Styling")
    
    def __unicode__(self):
        return "%s Stationary" % (self.name)

    class Meta:
        ordering = ['name',]
        verbose_name_plural = "Stationaries"
