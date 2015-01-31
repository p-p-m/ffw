from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class StaticPage(models.Model):
  title = models.CharField(max_length = 250)
  slug = models.SlugField(max_length = 250,unique = True)
  text = models.TextField()
  created = models.DateTimeField(auto_now_add = True)
  is_active = models.BooleanField(default = True)
  
  def __str__(self):
    return self.title 


class StaticPageImage(models.Model):
  static_page = models.ForeignKey(StaticPage, related_name = 'images')
  image = models.ImageField(upload_to = 'static pages/', verbose_name =
                            ('Image'))
  description = models.CharField(('Image description'), max_length = 127,
                                 blank = True)
