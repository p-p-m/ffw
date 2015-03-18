from gallery import models


def top_banner_processor(request):
    return {'top': models.Banner.objects.get(name='top')}
