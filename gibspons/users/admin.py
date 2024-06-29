from django.contrib import admin

from .models import User, Organisation, OTP


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "role", "is_approved", "organisation"]
    list_filter = ["role", "is_approved", "organisation"]
    search_fields = ["name", "email", "organisation__name"]


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ["name", "industry", "location", "logo", "created_at"]
    search_fields = ["name", "industry", "location"]


class OTPAdmin(admin.ModelAdmin):
    list_display = ["user", "value", "expiry_date"]
    search_fields = ["user__name", "value"]


admin.site.register(User, UserAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(OTP, OTPAdmin)
