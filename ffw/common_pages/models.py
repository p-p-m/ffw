
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class StaticPage(models.Model):
    class Meta:
        verbose_name = _('StaticPage')
        verbose_name_plural = _('StaticPages')

    title = models.CharField(_('StaticPage name'), max_length=250)
    slug = models.SlugField(_('StaticPage slug'), max_length=250, unique=True)
    text = models.TextField(_('StaticPage text'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    is_active = models.BooleanField(_('StaticPage is active'), default=True)

    def __str__(self):
        return self.title


class StaticPageImage(models.Model):
    class Meta:
        verbose_name = _('StaticPage Image')
        verbose_name_plural = _('StaticPage Images')

    staticpage = models.ForeignKey(StaticPage, related_name='images')
    photo = models.ImageField(upload_to='common_pages/static/common_pages', verbose_name=_('Photo'))
    description = models.CharField(_('Image description'), max_length=127, blank=True)
