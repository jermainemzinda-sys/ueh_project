from django.contrib import admin
from .models import Profile, Business, ServiceRequest, Opportunity, Application

admin.site.register(Profile)
admin.site.register(Business)
admin.site.register(ServiceRequest)
admin.site.register(Opportunity)
admin.site.register(Application)