from django.contrib import admin

from .models import Rapport


@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('label', 'state','type')
    list_filter = ('state',)
