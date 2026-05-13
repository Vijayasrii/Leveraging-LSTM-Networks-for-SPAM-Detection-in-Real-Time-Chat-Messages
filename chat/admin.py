from django.contrib import admin
from .models import Room, Message, OffensiveMessage

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)

@admin.register(OffensiveMessage)
class OffensiveMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'message', 'time')
    list_filter = ('user', 'room', 'time')
