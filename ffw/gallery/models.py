from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Banner(models.Model):
    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        
    name = models.CharField(_('Banner name'), max_length = 100)
    
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BannerImage(models.Model):
    class Meta:
        verbose_name = _('Banner Image')
        verbose_name_plural = _('Banner Images')
    
    banner = models.ForeignKey(Banner, related_name = 'images')
    image = models.ImageField(upload_to = 'static pages/',
                            verbose_name =_('Image'))
    url_image = models.CharField(_('URL'), max_length = 127,)
    description = models.CharField(_('Image description'), max_length=127,
                                   blank = True)
    is_active = models.BooleanField(_('Is image active'), 
                                           default = True)
    
    def __str__(self):
        return self.description

    
   


