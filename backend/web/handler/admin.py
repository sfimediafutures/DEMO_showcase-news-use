from django.contrib import admin
from handler.models import User, Session, Entry
# Register your models here.
admin.site.register(User)
admin.site.register(Session)
admin.site.register(Entry)

# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.filter_vertical
# The Genre page is wonky due to the nature of many to many, so if applicable this can be implemented
# as a filter_vertical.
