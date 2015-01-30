from django.db import models

class StaticPage(models.Model):
  title=models.CharField(max_length=250)
  slug=models.CharField(max_length=250)
  text=models.TextField()
  created=models.DateTimeField(auto_now_add=True)
  is_active=models.BooleanField(default=True)

  def __unicode__(self):
    return self.title 
