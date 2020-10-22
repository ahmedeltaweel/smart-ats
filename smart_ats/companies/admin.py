from django.contrib import admin
from .models import CompanyAdmin , Company
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html



@admin.register(CompanyAdmin)
class CompanyAdminSite(UserAdmin):
    model = CompanyAdmin

    list_display = ["username",'email','company']

    fieldsets = (
        ('Personal info', {'fields': ('first_name','last_name','username','email',)}),
        ('Company info',{'fields':('company','user_type')}),
        ("Additional info", {'fields': ('is_active','is_staff','date_joined','last_login',)}),
                )
    
    readonly_fields =['password','date_joined','last_login','user_type']

    add_fieldsets = (
        (None, {
            'fields': ('first_name','last_name','username','email', 'password1', 'password2',
                        'company','is_active','is_staff',
            )
            }
        ),)

    def save_model(self, request, obj, form, change):
        obj.user_type = 'admin'
        super().save_model(request, obj, form, change)


class StackedCompanyAdmin(admin.TabularInline):
    model = CompanyAdmin
    fields = ('username','email','is_active')
    readonly_fields = ('username', 'email')
    extra = 0

    def has_add_permission(self, request, *args, **kwargs):
        return False



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company

    list_display = ('id', 'name', 'Comapany_website','Company_Admin', 'is_active')

    list_filter = ('is_active',)

    search_fields = ("name__icontains", )

    readonly_fields = ('created','modified')

    inlines = (StackedCompanyAdmin,)


    def Comapany_website(self, obj):
        return format_html(f'<a href="{obj.website}">Website</a>')


    def Company_Admin(self, obj):
        url = str(reverse("admin:companies_companyadmin_changelist")
                +"?"
                + urlencode({"company__id": f"{obj.id}"}))
        
        return format_html(f"<a href='{url}'>company admins</a>")        
    
    Company_Admin.short_description = "Company Admins"