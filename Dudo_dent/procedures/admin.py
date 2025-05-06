from django.contrib import admin

from Dudo_dent.procedures.models import Procedure


# Register your models here.

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    pass

