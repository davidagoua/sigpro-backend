from django.contrib import admin
from .models import CommentaireTDR, TDR, TDRProgramme


@admin.register(TDR)
class TDRAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'label','activity', 'created', 'state', 'injonction', 'accorder')
    list_filter = ('state',)


@admin.register(CommentaireTDR)
class CommentaireTDRAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'content')


@admin.register(TDRProgramme)
class TDRProgrammeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'label','activity', 'created', 'state', 'injonction', 'accorder')
    list_filter = ('state',)
