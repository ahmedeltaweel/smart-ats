from django.contrib import admin

from .models import Company, CompanyAdmin

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyAdmin)
