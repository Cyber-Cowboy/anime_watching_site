from django.contrib import admin

from .models import Title, Episode, Translation, AnimeList, TitleInList

admin.site.register(Title)
admin.site.register(Episode)
admin.site.register(Translation)
admin.site.register(AnimeList)
admin.site.register(TitleInList)