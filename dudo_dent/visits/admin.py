from django.contrib import admin

from dudo_dent.visits.models import Visit


# Register your models here.


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_filter = ('date', 'patient', 'procedure')


