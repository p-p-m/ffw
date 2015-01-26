from django.db import models

# Create your models here.

class StaticPage(models.Model):
  title=models.CharField(max_length=250)
  slug=models.CharField(max_length=250)
  text=models.TextField()
  is_active=models.BooleanField(default=True)

  def __unicode__(self):
    return self.title
