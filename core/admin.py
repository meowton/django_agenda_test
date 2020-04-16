from django.contrib import admin
from core.models import Event

# Register your models here.
class EventDetails(admin.ModelAdmin):
    list_display = ("id", "title", "event_date", "created_date")
    list_filter = (
        "user",
        "event_date",
        "created_date",
    )


admin.site.register(Event, EventDetails)
