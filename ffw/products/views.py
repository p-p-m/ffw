from django.http import HttpResponse
from django.views.generic import View

from . import forms


class CommentListView(View):
    """ REST-like view that support only comments creation for now """

    def post(self, request):
        form = forms.CommentForm(request.POST)
        if not form.is_valid():
            return HttpResponse(dict(form.errors), status=400)
        form.save()
        return HttpResponse(status=201)
