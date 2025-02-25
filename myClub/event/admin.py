from django.contrib import admin
from .models import Event, Vanue, MyUser
from django.contrib.auth.models import Group
# Register your models here.

# admin.site.register(Event)
admin.site.register(Vanue)
#adding Vanue into my admin pannel
admin.site.register(MyUser)
#Removing Group 
admin.site.unregister(Group)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date',  'vanue','aproved')
    ordering = ('-date',) # descending order
    search_fields = ('title', 'description') 
    fields =  ('title','vanue', 'description', 'date', 'manager', 'aproved')
    list_filter = ('date', 'vanue')

