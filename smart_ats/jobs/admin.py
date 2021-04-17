from django.contrib import admin

from .models import Job, Category


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...
