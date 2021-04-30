from django.contrib import admin

from .models import Job, Category, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(JobApplication)
class JobApplication(admin.ModelAdmin):
    ...
