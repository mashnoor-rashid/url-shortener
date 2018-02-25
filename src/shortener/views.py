from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from analytics.models import ClickEvent

from .forms import SubmitUrlForm
from .models import MashURL


class HomeView(View):
    def get (self, request, *arkgs, **kwargs):
        form = SubmitUrlForm()
        context = {"form" : form, "title": "Mash URL Shortener"}
        return render(request, "shortener/home.html", context)

    def post (self, request, *arkgs, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {"form" : form, "title": "MashURL Shortener"}
        template = "shortener/home.html"

        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = MashURL.objects.get_or_create(url=new_url)
            context = {"object": obj, "created":created}
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template, context)

class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = MashURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        if ("https://" not in obj.url):
            obj.url = "https://" + obj.url
        return HttpResponseRedirect(obj.url)