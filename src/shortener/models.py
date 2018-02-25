from django.db import models
from django.conf import settings
from . utils import code_gen, create_shortcode
from .validators import validate_url, validate_dot_com
# from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse

# If not found, then default to 15. Helpful when copying app to diff project
# and don't copy over the settings file
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class MashURL_Manager(models.Manager):
    def all(self, *args, **kwargs):
        qs = super(MashURL_Manager, self).all(*args, **kwargs)
        # qs = qs.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        # Refresh X top codes specified, otherwise all
        qs = MashURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        num_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            num_codes += 1
        return "New codes made: {}".format(num_codes)

class MashURL(models.Model):
    url = models.CharField(max_length=250, validators=[validate_url, validate_dot_com])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    # Overriding default model manager
    objects = MashURL_Manager()

    def save(self, *args, **kwargs):
        if self.shortcode == None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        # Call the default save method
        super(MashURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
        # return "https://mashurl.com/{shortcode}".format(shortcode=self.shortcode)
        return url_path
