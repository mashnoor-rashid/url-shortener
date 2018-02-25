from django.db import models

from shortener.models import MashURL

class ClickEventManager(models.Manager):
    def create_event(self, mash_instance):
        if isinstance(mash_instance, MashURL):
            obj, created = self.get_or_create(mash_url=mash_instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    # 1 to 1 relationship with MashURL objects
    mash_url = models.OneToOneField(MashURL)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{}".format(self.count)
