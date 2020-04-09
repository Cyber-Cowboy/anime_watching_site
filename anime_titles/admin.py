from django.contrib import admin

from .models import Title, Episode, Translation

admin.site.register(Title)
admin.site.register(Episode)
admin.site.register(Translation)