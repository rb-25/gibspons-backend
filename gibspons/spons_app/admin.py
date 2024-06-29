from django.contrib import admin
from .models import Company, POC, Sponsorship, Event


class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ["company", "event", "poc", "status"]
    list_filter = ["company", "event", "status"]
    search_fields = ["company__name", "event__name"]


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "money_raised"]
    list_filter = ["start_date", "end_date"]
    search_fields = ["name"]


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "industry", "organisation"]
    list_filter = ["industry", "organisation"]
    search_fields = ["name"]


class POCAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "company"]
    list_filter = ["company"]
    search_fields = ["name", "email", "phone"]


admin.site.register(Event, EventAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(POC, POCAdmin)
admin.site.register(Sponsorship, SponsorshipAdmin)
