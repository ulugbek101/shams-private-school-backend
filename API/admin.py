from django.contrib import admin
from django.contrib.auth.models import Group

from . import models

admin.site.register(models.User)
admin.site.register(models.Subject)
admin.site.register(models.Group)
admin.site.register(models.Pupil)
admin.site.unregister(Group)
