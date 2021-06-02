from django.contrib import admin
from .models import Drama, Genre ,Episode , Cast , Like,DramaList, Room

admin.site.register(Drama)
admin.site.register(Genre)
admin.site.register(Episode)
admin.site.register(Cast)
admin.site.register(Like)
admin.site.register(DramaList)
admin.site.register(Room)
# Register your models here.
