from django.contrib import admin
from .models import UserCollections, VisitorsCount

from import_export.admin import ImportExportModelAdmin


@admin.register(UserCollections)
class ViewAdmin(ImportExportModelAdmin):
    search_fields = ('title', 'description', 'genres', 'uuid')
    odering = ['title']


@admin.register(VisitorsCount)
class ViewAdmin(ImportExportModelAdmin):
    pass