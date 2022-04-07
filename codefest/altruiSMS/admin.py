from django.contrib import admin
from .models import Beneficiary, Organization,Event

admin.site.register(Beneficiary)
admin.site.register(Organization)
admin.site.register(Event)