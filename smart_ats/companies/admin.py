from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from smart_ats.users.models import User

from .models import Company, CompanyAdmin


@admin.register(CompanyAdmin)
class CompanyAdminAdmin(UserAdmin):
    list_display = ["username", "email", "company"]

    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                )
            },
        ),
        ("Company info", {"fields": ("company", "user_type")}),
        (
            "Additional info",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )

    readonly_fields = ["password", "date_joined", "last_login", "user_type"]

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "company",
                    "is_active",
                    "is_staff",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.user_type = User.STATUSES.admin
        super().save_model(request, obj, form, change)


class StackedCompanyAdmin(admin.TabularInline):
    model = CompanyAdmin
    fields = ("username", "email", "is_active")
    readonly_fields = ("username", "email")
    extra = 0

    def has_add_permission(self, request, *args, **kwargs):
        return False


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "comapany_website", "company_admin", "is_active")

    list_filter = ("is_active",)

    search_fields = ("name__icontains",)

    readonly_fields = ("created", "modified")

    inlines = (StackedCompanyAdmin,)

    def comapany_website(self, obj):
        return format_html(f'<a href="{obj.website}">Website</a>')

    def company_admin(self, obj):
        url = str(
            reverse("admin:companies_companyadmin_changelist")
            + "?"
            + urlencode({"company__id": f"{obj.id}"})
        )

        return format_html(f"<a href='{url}'>company admins</a>")

    company_admin.short_description = "Company Admins"
