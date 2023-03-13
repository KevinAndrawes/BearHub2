from django.contrib import admin
from BearHubHome.models import Student, Event, AdminUser, EventRequest
# Register your models here.
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(AdminUser)
admin.site.register(EventRequest)