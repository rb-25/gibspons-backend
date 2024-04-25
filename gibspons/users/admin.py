from django.contrib import admin

from .models import User, Organisation,OTP

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(OTP)
