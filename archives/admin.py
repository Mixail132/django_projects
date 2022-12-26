from django.contrib import admin
from .models import Archives


class ArchivesAdmin(admin.ModelAdmin):
    list_display = ("dat", "usd", "eur", "rub",)


admin.site.register(Archives, ArchivesAdmin)

# Register your models here.
