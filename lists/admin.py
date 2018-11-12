from django.contrib import admin

# Register your models here.
from .models import List, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class ListAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(List, ListAdmin)