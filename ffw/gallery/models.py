from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import URLValidator


@python_2_unicode_compatible
class Banner(models.Model):
    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    name = models.CharField(_('Banner name'), max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BannerImage(models.Model):
    class Meta:
        verbose_name = _('Banner Image')
        verbose_name_plural = _('Banner Images')

    banner = models.ForeignKey(Banner, related_name='images')
    photo = models.ImageField(upload_to='gallery', verbose_name=('Photo'))
    link = models.URLField(_('Link'), max_length=127, default='', validators=[URLValidator], blank=True)
    description = models.CharField(_('Image description'), max_length=127, blank=True)
    is_active = models.BooleanField(_('Is image active'), default=True)

    def __str__(self):
        return 'Banner: ' + self.banner.name + ' - ' + self.description


@python_2_unicode_compatible
class GalleryImage(models.Model):
    class Meta:
        verbose_name = _('Gallery Image')
        verbose_name_plural = _('Gallery Images')

    photo = models.ImageField(upload_to='gallery/gallery', verbose_name=('Photo'))
    link = models.URLField(_('Link'), max_length=127, default='', validators=[URLValidator])
    description = models.CharField(_('Image description'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Is image active'), default=True)

    def __str__(self):
        return  self.description
