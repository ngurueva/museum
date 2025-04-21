from django.contrib import admin
from .models import Event, EventSchedule

class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'capacity', 'is_visible']
    list_filter = ['event_type', 'is_visible']
    search_fields = ['name', 'description']
    ordering = ['name']
    inlines = [EventScheduleInline]

